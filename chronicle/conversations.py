"""
Chronicle Conversations - Multi-turn dialogue with historical perspective.

Maintains conversation state and context for follow-up questions.
"""

import os
import sqlite3
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

import anthropic

from .patterns import library, Pattern


# Configuration
CONVERSATIONS_DB = Path(__file__).parent.parent / "conversations.db"
SESSION_TTL_HOURS = 24  # Sessions expire after 24 hours


@dataclass
class Message:
    """A single message in a conversation."""
    role: str  # "user" or "assistant"
    content: str
    patterns_used: list[str] = field(default_factory=list)  # Pattern IDs referenced
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass 
class Conversation:
    """A multi-turn conversation session."""
    session_id: str
    messages: list[Message]
    created_at: str
    last_accessed: str
    
    def add_user_message(self, content: str) -> Message:
        msg = Message(role="user", content=content)
        self.messages.append(msg)
        self.last_accessed = datetime.utcnow().isoformat()
        return msg
    
    def add_assistant_message(self, content: str, patterns_used: list[str] = None) -> Message:
        msg = Message(role="assistant", content=content, patterns_used=patterns_used or [])
        self.messages.append(msg)
        self.last_accessed = datetime.utcnow().isoformat()
        return msg
    
    def get_context_summary(self) -> str:
        """Summarize conversation for context window efficiency."""
        if len(self.messages) <= 4:
            return ""
        
        # For longer conversations, summarize earlier exchanges
        early_messages = self.messages[:-4]
        topics = set()
        patterns = set()
        
        for msg in early_messages:
            if msg.patterns_used:
                patterns.update(msg.patterns_used)
        
        if patterns:
            return f"[Earlier in this conversation, we discussed patterns: {', '.join(patterns)}]"
        return ""
    
    def to_anthropic_messages(self) -> list[dict]:
        """Convert to Anthropic API message format."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]


class ConversationStore:
    """Persistent storage for conversations."""
    
    def __init__(self, db_path: Path = CONVERSATIONS_DB):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database schema."""
        db = sqlite3.connect(str(self.db_path))
        db.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                messages TEXT,  -- JSON array
                created_at TEXT,
                last_accessed TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_last_accessed 
            ON conversations(last_accessed);
        """)
        db.commit()
        db.close()
    
    def create(self) -> Conversation:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())[:8]
        now = datetime.utcnow().isoformat()
        
        conv = Conversation(
            session_id=session_id,
            messages=[],
            created_at=now,
            last_accessed=now,
        )
        
        self._save(conv)
        return conv
    
    def get(self, session_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by session ID."""
        db = sqlite3.connect(str(self.db_path))
        row = db.execute(
            "SELECT session_id, messages, created_at, last_accessed FROM conversations WHERE session_id = ?",
            (session_id,)
        ).fetchone()
        db.close()
        
        if not row:
            return None
        
        messages_data = json.loads(row[1])
        messages = [
            Message(
                role=m["role"],
                content=m["content"],
                patterns_used=m.get("patterns_used", []),
                timestamp=m.get("timestamp", ""),
            )
            for m in messages_data
        ]
        
        return Conversation(
            session_id=row[0],
            messages=messages,
            created_at=row[2],
            last_accessed=row[3],
        )
    
    def _save(self, conv: Conversation):
        """Save a conversation to the database."""
        messages_json = json.dumps([
            {
                "role": m.role,
                "content": m.content,
                "patterns_used": m.patterns_used,
                "timestamp": m.timestamp,
            }
            for m in conv.messages
        ])
        
        db = sqlite3.connect(str(self.db_path))
        db.execute("""
            INSERT OR REPLACE INTO conversations 
            (session_id, messages, created_at, last_accessed)
            VALUES (?, ?, ?, ?)
        """, (conv.session_id, messages_json, conv.created_at, conv.last_accessed))
        db.commit()
        db.close()
    
    def update(self, conv: Conversation):
        """Update an existing conversation."""
        self._save(conv)
    
    def cleanup_expired(self):
        """Remove expired sessions."""
        cutoff = (datetime.utcnow() - timedelta(hours=SESSION_TTL_HOURS)).isoformat()
        
        db = sqlite3.connect(str(self.db_path))
        db.execute("DELETE FROM conversations WHERE last_accessed < ?", (cutoff,))
        db.commit()
        db.close()


# System prompt for conversations
CONVERSATION_SYSTEM_PROMPT = """You are Chronicle, a perspective engine that helps people understand their present situation through the lens of deep time.

You're in a conversation. The user may ask follow-up questions, probe deeper into specific patterns, or explore tangents. Maintain context from earlier in the conversation.

Your role:
1. Connect present concerns to historical patterns
2. Synthesize perspective that is grounded, calibrated, and useful
3. Engage naturally in dialogue—you can ask clarifying questions, admit uncertainty, and explore ideas together

Guidelines:
- History rhymes but doesn't repeat. Be precise about what transfers and what doesn't.
- Acknowledge uncertainty. You're not predicting, you're providing perspective.
- Contemporary observers were often wrong. Distinguish their views from hindsight.
- Multiple interpretations of history exist. Note when relevant.
- Be concrete and specific. Use examples from patterns provided.
- For follow-ups, build on what was discussed earlier—don't repeat everything.
- If the user wants to explore a tangent, go with them.
- You can ask clarifying questions if the user's concern is vague.

When you first respond to a question, structure your response as:
1. **Historical Rhymes** — What patterns are relevant?
2. **What Actually Happened** — Outcomes in those cases
3. **Calibration** — How to size their concern/excitement
4. **What's Different** — Genuine novelty to watch
5. **Perspective Shift** — A useful reframe

For follow-ups, respond more conversationally—you don't need the full structure."""


class ConversationEngine:
    """Engine for multi-turn perspective conversations."""
    
    def __init__(
        self,
        store: Optional[ConversationStore] = None,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
    ):
        self.store = store or ConversationStore()
        self.model = model
        
        # Get API key from multiple sources
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            config_paths = [
                os.path.expanduser("~/.anthropic/api_key"),
                os.path.expanduser("~/.config/anthropic/api_key"),
            ]
            for path in config_paths:
                if os.path.exists(path):
                    with open(path) as f:
                        key = f.read().strip()
                    break
        
        self.client = anthropic.Anthropic(api_key=key) if key else None
        library.load()
    
    def start_conversation(self) -> Conversation:
        """Start a new conversation session."""
        return self.store.create()
    
    def send_message(
        self,
        session_id: str,
        user_message: str,
        max_patterns: int = 5,
        api_key: Optional[str] = None,
    ) -> tuple[Conversation, str]:
        """
        Send a message in a conversation and get a response.
        
        Returns (updated conversation, assistant response text).
        """
        conv = self.store.get(session_id)
        if not conv:
            raise ValueError(f"Session {session_id} not found")
        
        # Add user message
        conv.add_user_message(user_message)
        
        # Check for API client
        client = self.client
        if api_key:
            client = anthropic.Anthropic(api_key=api_key)
        
        if not client:
            response = "No API key configured. Set ANTHROPIC_API_KEY or provide one in the request."
            conv.add_assistant_message(response)
            self.store.update(conv)
            return conv, response
        
        # Find relevant patterns for the current question
        patterns = self._find_relevant_patterns(user_message, max_patterns)
        
        # Build system prompt with pattern context
        system = CONVERSATION_SYSTEM_PROMPT
        if patterns:
            patterns_context = "\n\n---\n\n".join(p.to_context() for p in patterns)
            system += f"\n\n---\n\nAVAILABLE HISTORICAL PATTERNS:\n\n{patterns_context}"
        
        # Add conversation context summary for long conversations
        context_summary = conv.get_context_summary()
        if context_summary:
            system += f"\n\n{context_summary}"
        
        # Generate response
        response = client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system,
            messages=conv.to_anthropic_messages(),
        )
        
        assistant_text = response.content[0].text
        pattern_ids = [p.id for p in patterns]
        
        conv.add_assistant_message(assistant_text, pattern_ids)
        self.store.update(conv)
        
        return conv, assistant_text
    
    def _find_relevant_patterns(
        self,
        question: str,
        max_patterns: int,
    ) -> list[Pattern]:
        """Find patterns relevant to a question."""
        # Try semantic search first
        try:
            from .embeddings import semantic_search_api
            results = semantic_search_api(question, limit=max_patterns)
            if results and results[0].get("similarity", 0) > 0.3:
                pattern_ids = [r["id"] for r in results]
                return [library.get(pid) for pid in pattern_ids if library.get(pid)]
        except Exception:
            pass
        
        # Fall back to keyword search
        return library.search_simple(question)[:max_patterns]
    
    def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """Get a conversation by session ID."""
        return self.store.get(session_id)


# Default engine instance
conversation_engine = ConversationEngine()
