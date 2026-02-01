"""
Chronicle Embeddings - Generate and query vector embeddings for patterns.

Uses embeddinggemma-300M via llama.cpp for local embedding generation.
Stores vectors in sqlite-vec for fast similarity search.
"""

import os
import json
import sqlite3
import struct
import subprocess
from pathlib import Path
from typing import Optional

import sqlite_vec

from .patterns import library, Pattern


# Paths
MODELS_DIR = Path.home() / ".cache" / "qmd" / "models"
EMBEDDING_MODEL = "hf_ggml-org_embeddinggemma-300M-Q8_0.gguf"
VECTORS_DB = Path(__file__).parent.parent / "vectors.db"


def get_model_path() -> Path:
    """Get path to embedding model."""
    model_path = MODELS_DIR / EMBEDDING_MODEL
    if not model_path.exists():
        raise FileNotFoundError(
            f"Embedding model not found at {model_path}. "
            "Run 'qmd pull --refresh' to download models."
        )
    return model_path


def embed_text_llama(text: str, model_path: Path) -> list[float]:
    """Generate embedding using llama.cpp's llama-embedding CLI."""
    # Find llama-embedding binary
    llama_bin = None
    for path in [
        Path("/opt/homebrew/bin/llama-embedding"),
        Path("/usr/local/bin/llama-embedding"),
        Path.home() / ".local" / "bin" / "llama-embedding",
    ]:
        if path.exists():
            llama_bin = path
            break
    
    if not llama_bin:
        raise FileNotFoundError(
            "llama-embedding not found. Install llama.cpp: "
            "brew install llama.cpp"
        )
    
    # Run embedding with JSON array output format
    result = subprocess.run(
        [
            str(llama_bin),
            "-m", str(model_path),
            "--embd-normalize", "2",  # L2 normalize
            "--embd-output-format", "array",  # Output as JSON arrays
            "-p", text[:8000],  # Truncate to avoid context overflow
        ],
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Embedding failed: {result.stderr}")
    
    # Parse output - with "array" format, it outputs [[...]] JSON
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if line.startswith('[[') or line.startswith('['):
            try:
                parsed = json.loads(line)
                # If it's [[...]], take the first embedding
                if parsed and isinstance(parsed[0], list):
                    return parsed[0]
                return parsed
            except json.JSONDecodeError:
                continue
    
    raise RuntimeError(f"Could not parse embedding output: {result.stdout[:500]}")


def serialize_embedding(embedding: list[float]) -> bytes:
    """Serialize embedding to bytes for sqlite-vec."""
    return struct.pack(f'{len(embedding)}f', *embedding)


def deserialize_embedding(data: bytes) -> list[float]:
    """Deserialize embedding from bytes."""
    n = len(data) // 4
    return list(struct.unpack(f'{n}f', data))


def init_db(db_path: Path = VECTORS_DB) -> sqlite3.Connection:
    """Initialize the vectors database."""
    db = sqlite3.connect(str(db_path))
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    # Create tables
    db.executescript("""
        CREATE TABLE IF NOT EXISTS patterns (
            id TEXT PRIMARY KEY,
            title TEXT,
            domain TEXT,
            summary TEXT,
            content_hash TEXT
        );
        
        CREATE VIRTUAL TABLE IF NOT EXISTS pattern_vectors USING vec0(
            id TEXT PRIMARY KEY,
            embedding float[768]
        );
    """)
    
    return db


def index_patterns(force: bool = False) -> dict:
    """Index all patterns with embeddings."""
    library.load()
    model_path = get_model_path()
    
    db = init_db()
    stats = {"indexed": 0, "skipped": 0, "errors": 0}
    
    for pattern in library.all():
        try:
            # Check if already indexed (by content hash)
            content_hash = str(hash(pattern.content))
            existing = db.execute(
                "SELECT content_hash FROM patterns WHERE id = ?",
                (pattern.id,)
            ).fetchone()
            
            if existing and existing[0] == content_hash and not force:
                stats["skipped"] += 1
                continue
            
            # Generate embedding from summary + key content
            text_to_embed = f"{pattern.title}\n\n{pattern.summary}\n\n{pattern.content[:4000]}"
            embedding = embed_text_llama(text_to_embed, model_path)
            
            # Upsert pattern metadata
            db.execute("""
                INSERT OR REPLACE INTO patterns (id, title, domain, summary, content_hash)
                VALUES (?, ?, ?, ?, ?)
            """, (pattern.id, pattern.title, pattern.domain, pattern.summary, content_hash))
            
            # Upsert embedding
            db.execute("DELETE FROM pattern_vectors WHERE id = ?", (pattern.id,))
            db.execute(
                "INSERT INTO pattern_vectors (id, embedding) VALUES (?, ?)",
                (pattern.id, serialize_embedding(embedding))
            )
            
            db.commit()
            stats["indexed"] += 1
            print(f"  ✓ {pattern.id}")
            
        except Exception as e:
            stats["errors"] += 1
            print(f"  ✗ {pattern.id}: {e}")
    
    db.close()
    return stats


def semantic_search(query: str, limit: int = 5, db_path: Path = VECTORS_DB) -> list[dict]:
    """Search patterns by semantic similarity."""
    if not db_path.exists():
        raise FileNotFoundError(
            f"Vector database not found at {db_path}. "
            "Run 'chronicle embed' to generate embeddings."
        )
    
    model_path = get_model_path()
    query_embedding = embed_text_llama(query, model_path)
    
    db = sqlite3.connect(str(db_path))
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    # Vector similarity search
    results = db.execute("""
        SELECT 
            p.id,
            p.title,
            p.domain,
            p.summary,
            vec_distance_cosine(v.embedding, ?) as distance
        FROM pattern_vectors v
        JOIN patterns p ON v.id = p.id
        ORDER BY distance ASC
        LIMIT ?
    """, (serialize_embedding(query_embedding), limit)).fetchall()
    
    db.close()
    
    return [
        {
            "id": r[0],
            "title": r[1],
            "domain": r[2],
            "summary": r[3],
            "similarity": 1 - r[4],  # Convert distance to similarity
        }
        for r in results
    ]


def embed_text_openai(text: str, api_key: str) -> list[float]:
    """Generate embedding using OpenAI API."""
    import openai
    
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:8000],
    )
    return response.data[0].embedding


def semantic_search_api(
    query: str, 
    api_key: Optional[str] = None,
    limit: int = 5, 
    db_path: Path = VECTORS_DB
) -> list[dict]:
    """
    Semantic search using OpenAI embeddings for the query.
    Falls back to keyword search if no API key or vectors.db unavailable.
    """
    # Check for API key
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    
    if not api_key or not db_path.exists():
        # Fall back to keyword search
        return search_keyword(query, limit, db_path)
    
    try:
        # Get query embedding from OpenAI
        query_embedding = embed_text_openai(query, api_key)
        
        # Note: OpenAI text-embedding-3-small outputs 1536 dims by default
        # Our local embeddings are 768 dims, so we need to handle this
        # For now, fall back to keyword if dimensions don't match
        if len(query_embedding) != 768:
            # Try with dimension reduction parameter
            import openai
            client = openai.OpenAI(api_key=api_key)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=query[:8000],
                dimensions=768,  # Request specific dimensions
            )
            query_embedding = response.data[0].embedding
        
        db = sqlite3.connect(str(db_path))
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        db.enable_load_extension(False)
        
        # Vector similarity search
        results = db.execute("""
            SELECT 
                p.id,
                p.title,
                p.domain,
                p.summary,
                vec_distance_cosine(v.embedding, ?) as distance
            FROM pattern_vectors v
            JOIN patterns p ON v.id = p.id
            ORDER BY distance ASC
            LIMIT ?
        """, (serialize_embedding(query_embedding), limit)).fetchall()
        
        db.close()
        
        return [
            {
                "id": r[0],
                "title": r[1],
                "domain": r[2],
                "summary": r[3],
                "similarity": 1 - r[4],
            }
            for r in results
        ]
        
    except Exception as e:
        # Fall back to keyword search on any error
        print(f"Semantic search failed, falling back to keyword: {e}")
        return search_keyword(query, limit, db_path)


def search_keyword(query: str, limit: int = 5, db_path: Path = VECTORS_DB) -> list[dict]:
    """Keyword-based search fallback."""
    if db_path.exists():
        db = sqlite3.connect(str(db_path))
        results = db.execute("""
            SELECT id, title, domain, summary
            FROM patterns
            WHERE title LIKE ? OR summary LIKE ? OR domain LIKE ?
            LIMIT ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%", limit)).fetchall()
        db.close()
        
        if results:
            return [
                {
                    "id": r[0],
                    "title": r[1],
                    "domain": r[2],
                    "summary": r[3],
                    "similarity": 0.5,  # Keyword match placeholder
                }
                for r in results
            ]
    
    # Fall back to library search
    library.load()
    results = library.search_simple(query)[:limit]
    return [
        {
            "id": p.id,
            "title": p.title,
            "domain": p.domain,
            "summary": p.summary,
            "similarity": 0.5,
        }
        for p in results
    ]


def search_without_model(query: str, limit: int = 5, db_path: Path = VECTORS_DB) -> list[dict]:
    """
    Search using pre-computed query embedding (for deployment without local model).
    Falls back to keyword search if no embedding available.
    """
    # Try semantic search with OpenAI first
    return semantic_search_api(query, limit=limit, db_path=db_path)
