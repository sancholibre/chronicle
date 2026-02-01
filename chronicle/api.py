"""
Chronicle HTTP API - Simple REST endpoint for agents and applications.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .patterns import library
from .synthesis import SynthesisEngine, Perspective


# --- Models ---

class PerspectiveRequest(BaseModel):
    """Request for historical perspective."""
    question: str
    max_patterns: int = 5
    domains: Optional[list[str]] = None
    api_key: Optional[str] = None  # BYOK support


class PatternSummary(BaseModel):
    """Brief pattern info for API responses."""
    id: str
    title: str
    domain: str
    era: str


class PerspectiveResponse(BaseModel):
    """Response with synthesized perspective."""
    question: str
    synthesis: str
    confidence: str
    caveats: list[str]
    patterns_used: list[PatternSummary]


class PatternDetail(BaseModel):
    """Full pattern details."""
    id: str
    title: str
    domain: str
    era: str
    time_scale: str
    confidence: str
    summary: str
    content: str


class SearchResult(BaseModel):
    """Pattern search result."""
    id: str
    title: str
    domain: str
    era: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    patterns_loaded: int
    version: str


# --- App ---

app = FastAPI(
    title="Chronicle API",
    description="Historical perspective engine for AI agents",
    version="0.1.0",
)

# CORS for browser-based agents
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def landing():
    """Landing page with Chronicle intro."""
    library.load()
    pattern_count = len(library.patterns)
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronicle - Historical Perspective Engine</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .container {{
            max-width: 700px;
            text-align: center;
        }}
        h1 {{
            font-size: 3rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(90deg, #f39c12, #e74c3c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .tagline {{
            font-size: 1.3rem;
            color: #888;
            margin-bottom: 2rem;
        }}
        .description {{
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 2rem;
            color: #bbb;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-bottom: 2rem;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #f39c12;
        }}
        .stat-label {{
            font-size: 0.9rem;
            color: #888;
        }}
        .links {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        a {{
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: #f39c12;
            color: #1a1a2e;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s, background 0.2s;
        }}
        a:hover {{
            transform: translateY(-2px);
            background: #e67e22;
        }}
        a.secondary {{
            background: transparent;
            border: 2px solid #f39c12;
            color: #f39c12;
        }}
        a.secondary:hover {{
            background: rgba(243, 156, 18, 0.1);
        }}
        .footer {{
            margin-top: 3rem;
            font-size: 0.9rem;
            color: #666;
        }}
        .footer a {{
            background: none;
            padding: 0;
            color: #888;
            font-weight: normal;
        }}
        .footer a:hover {{
            color: #f39c12;
            transform: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Chronicle</h1>
        <p class="tagline">Historical perspective for present decisions</p>
        
        <p class="description">
            Every major moment feels unprecedented to those living through it. 
            But most "unprecedented" situations rhyme with something from the past.
            Chronicle surfaces those rhymes—not to predict the future, but to provide perspective.
        </p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{pattern_count}</div>
                <div class="stat-label">Historical Patterns</div>
            </div>
            <div class="stat">
                <div class="stat-value">5</div>
                <div class="stat-label">Domains</div>
            </div>
        </div>
        
        <div class="links">
            <a href="/docs">Interactive API Docs</a>
            <a href="/patterns" class="secondary">Browse Patterns</a>
            <a href="https://github.com/sancholibre/chronicle" class="secondary">GitHub</a>
        </div>
        
        <p class="footer">
            Built by <a href="https://deaconsantiago.com/willie">Willie 🦣</a> — a woolly mammoth who believes precedent is grounding.
        </p>
    </div>
</body>
</html>
"""


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    library.load()
    return HealthResponse(
        status="ok",
        patterns_loaded=len(library.patterns),
        version="0.1.0",
    )


@app.get("/patterns", response_model=list[SearchResult])
async def list_patterns(domain: Optional[str] = None):
    """List all available patterns."""
    library.load()
    
    if domain:
        patterns = library.by_domain(domain)
    else:
        patterns = library.all()
    
    return [
        SearchResult(
            id=p.id,
            title=p.title,
            domain=p.domain,
            era=p.era,
        )
        for p in patterns
    ]


@app.get("/patterns/{pattern_id}", response_model=PatternDetail)
async def get_pattern(pattern_id: str):
    """Get a specific pattern by ID."""
    pattern = library.get(pattern_id)
    
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_id}' not found")
    
    return PatternDetail(
        id=pattern.id,
        title=pattern.title,
        domain=pattern.domain,
        era=pattern.era,
        time_scale=pattern.time_scale,
        confidence=pattern.confidence,
        summary=pattern.summary,
        content=pattern.content,
    )


@app.get("/search", response_model=list[SearchResult])
async def search_patterns(q: str):
    """Search patterns by keyword."""
    results = library.search_simple(q)
    
    return [
        SearchResult(
            id=p.id,
            title=p.title,
            domain=p.domain,
            era=p.era,
        )
        for p in results
    ]


class SemanticSearchRequest(BaseModel):
    """Request for semantic search."""
    query: str
    limit: int = 5
    api_key: Optional[str] = None  # OpenAI API key for embedding


class SemanticSearchResult(BaseModel):
    """Semantic search result with similarity score."""
    id: str
    title: str
    domain: str
    summary: str
    similarity: float


@app.post("/semantic-search", response_model=list[SemanticSearchResult])
async def semantic_search(request: SemanticSearchRequest):
    """
    Search patterns by semantic similarity.
    
    Uses OpenAI embeddings to find patterns semantically related to your query,
    even if they don't contain the exact keywords.
    
    Requires OpenAI API key - either set OPENAI_API_KEY environment variable,
    or pass api_key in the request body (BYOK).
    
    Falls back to keyword search if no API key provided.
    """
    from .embeddings import semantic_search_api
    
    results = semantic_search_api(
        query=request.query,
        api_key=request.api_key,
        limit=request.limit,
    )
    
    return [
        SemanticSearchResult(
            id=r["id"],
            title=r["title"],
            domain=r["domain"],
            summary=r["summary"],
            similarity=r["similarity"],
        )
        for r in results
    ]


@app.get("/domains")
async def list_domains():
    """List available domains with pattern counts."""
    library.load()
    
    domain_counts = {}
    for pattern in library.all():
        domain_counts[pattern.domain] = domain_counts.get(pattern.domain, 0) + 1
    
    return domain_counts


@app.post("/perspective", response_model=PerspectiveResponse)
async def get_perspective(request: PerspectiveRequest):
    """
    Get historical perspective on a question.
    
    This is the main endpoint. Provide a question about your current situation,
    and Chronicle will find relevant historical patterns and synthesize perspective.
    
    Requires API key - either set ANTHROPIC_API_KEY environment variable,
    or pass api_key in the request body (BYOK).
    """
    # Use provided API key or fall back to environment
    api_key = request.api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    # Create engine with appropriate key
    engine = SynthesisEngine(api_key=api_key)
    
    try:
        result = engine.generate_perspective(
            question=request.question,
            max_patterns=request.max_patterns,
            domains=request.domains,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return PerspectiveResponse(
        question=result.question,
        synthesis=result.synthesis,
        confidence=result.confidence,
        caveats=result.caveats,
        patterns_used=[
            PatternSummary(
                id=p.id,
                title=p.title,
                domain=p.domain,
                era=p.era,
            )
            for p in result.patterns_used
        ],
    )


# --- Entry point ---

def run(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()
