"""
Chronicle HTTP API - Simple REST endpoint for agents and applications.
"""

import os
import markdown
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .patterns import library
from .synthesis import SynthesisEngine, Perspective
from .conversations import ConversationEngine, conversation_engine
from . import templates


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


@app.get("/app", response_class=HTMLResponse)
async def app_page():
    """Main interactive UI for asking questions."""
    library.load()
    
    domains = {}
    for pattern in library.all():
        domains[pattern.domain] = domains.get(pattern.domain, 0) + 1
    
    return templates.app_page(
        pattern_count=len(library.patterns),
        domains=domains,
    )


@app.get("/browse", response_class=HTMLResponse)
async def browse_page(domain: Optional[str] = Query(None)):
    """Browse all patterns with optional domain filter."""
    library.load()
    
    domains = {}
    for pattern in library.all():
        domains[pattern.domain] = domains.get(pattern.domain, 0) + 1
    
    if domain:
        patterns = library.by_domain(domain)
    else:
        patterns = library.all()
    
    pattern_list = [
        {
            "id": p.id,
            "title": p.title,
            "domain": p.domain,
            "era": p.era,
        }
        for p in patterns
    ]
    
    return templates.browse_page(
        patterns=pattern_list,
        domains=domains,
        current_domain=domain,
    )


@app.get("/browse/{pattern_id}", response_class=HTMLResponse)
async def pattern_page(pattern_id: str):
    """View a single pattern in detail."""
    pattern = library.get(pattern_id)
    
    if not pattern:
        raise HTTPException(status_code=404, detail=f"Pattern '{pattern_id}' not found")
    
    # Convert markdown content to HTML
    content_html = markdown.markdown(
        pattern.content,
        extensions=['tables', 'fenced_code'],
    )
    
    return templates.pattern_detail_page(
        pattern={
            "id": pattern.id,
            "title": pattern.title,
            "domain": pattern.domain,
            "era": pattern.era,
            "time_scale": pattern.time_scale,
            "confidence": pattern.confidence,
        },
        content_html=content_html,
    )


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
async def list_patterns(
    request: Request,
    domain: Optional[str] = None,
):
    """List all available patterns. Redirects browsers to /browse."""
    # If browser, redirect to human-friendly page
    accept = request.headers.get("accept", "")
    if "text/html" in accept and "application/json" not in accept:
        from fastapi.responses import RedirectResponse
        url = "/browse" + (f"?domain={domain}" if domain else "")
        return RedirectResponse(url=url, status_code=302)
    
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


@app.get("/ask")
async def ask_simple(
    q: str = Query(..., description="Your question about the current situation"),
    patterns: int = Query(5, ge=1, le=10, description="Max patterns to consider"),
    api_key: Optional[str] = Query(None, description="Anthropic API key (BYOK)"),
):
    """
    Simple GET endpoint for quick queries.
    
    Example: /ask?q=Is AI hype like the dotcom bubble?
    
    Returns plain text synthesis for easy consumption.
    Requires API key via query param or ANTHROPIC_API_KEY env var.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    if not key:
        raise HTTPException(
            status_code=401, 
            detail="API key required. Pass ?api_key=YOUR_KEY or set ANTHROPIC_API_KEY env var."
        )
    
    engine = SynthesisEngine(api_key=key)
    
    try:
        result = engine.generate_perspective(question=q, max_patterns=patterns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return structured but simple response
    return {
        "question": result.question,
        "synthesis": result.synthesis,
        "confidence": result.confidence,
        "patterns": [p.title for p in result.patterns_used],
    }


class UnprecedentedRequest(BaseModel):
    """Request to check if something is truly unprecedented."""
    claim: str
    api_key: Optional[str] = None


class UnprecedentedResponse(BaseModel):
    """Response assessing whether something is unprecedented."""
    claim: str
    verdict: str  # "unprecedented", "has_precedent", or "partially_unprecedented"
    precedents: list[str]  # Brief list of historical parallels
    what_is_new: str  # What actually IS new about this situation
    what_rhymes: str  # What rhymes with history
    confidence: str


@app.post("/unprecedented")
async def check_unprecedented(request: UnprecedentedRequest):
    """
    The "Actually..." endpoint.
    
    When someone claims something is unprecedented, Chronicle checks history.
    Returns a verdict on whether it really is unprecedented, and what the
    historical parallels are.
    
    Great for grounding hyperbolic claims.
    """
    api_key = request.api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Pass api_key in body or set ANTHROPIC_API_KEY env var."
        )
    
    # Reframe as a perspective question
    question = f"Is this unprecedented: {request.claim}"
    
    engine = SynthesisEngine(api_key=api_key)
    
    try:
        result = engine.generate_perspective(question=question, max_patterns=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Parse the synthesis to extract verdict
    synthesis_lower = result.synthesis.lower()
    
    if "unprecedented" in synthesis_lower and "not unprecedented" not in synthesis_lower:
        if "partially" in synthesis_lower or "some aspects" in synthesis_lower:
            verdict = "partially_unprecedented"
        elif "truly unprecedented" in synthesis_lower or "genuinely unprecedented" in synthesis_lower:
            verdict = "unprecedented"
        else:
            verdict = "has_precedent"
    else:
        verdict = "has_precedent"
    
    return UnprecedentedResponse(
        claim=request.claim,
        verdict=verdict,
        precedents=[p.title for p in result.patterns_used],
        what_is_new="See synthesis for details.",
        what_rhymes="See synthesis for historical parallels.",
        confidence=result.confidence,
    )


# --- Conversation Models ---

class ConversationStartResponse(BaseModel):
    """Response when starting a new conversation."""
    session_id: str
    message: str


class ConversationMessageRequest(BaseModel):
    """Request to send a message in a conversation."""
    message: str
    max_patterns: int = 5
    api_key: Optional[str] = None


class ConversationMessage(BaseModel):
    """A message in a conversation."""
    role: str
    content: str
    patterns_used: list[str] = []
    timestamp: str


class ConversationResponse(BaseModel):
    """Response from a conversation message."""
    session_id: str
    response: str
    patterns_used: list[PatternSummary]
    message_count: int


class ConversationHistoryResponse(BaseModel):
    """Full conversation history."""
    session_id: str
    messages: list[ConversationMessage]
    created_at: str


# --- Conversation Endpoints ---

@app.post("/conversation/start", response_model=ConversationStartResponse)
async def start_conversation():
    """
    Start a new conversation session.
    
    Returns a session_id to use for subsequent messages.
    Conversations expire after 24 hours of inactivity.
    """
    conv = conversation_engine.start_conversation()
    return ConversationStartResponse(
        session_id=conv.session_id,
        message="Conversation started. Ask me about any situation you're facing, and I'll find historical parallels.",
    )


@app.post("/conversation/{session_id}", response_model=ConversationResponse)
async def send_conversation_message(session_id: str, request: ConversationMessageRequest):
    """
    Send a message in an existing conversation.
    
    The conversation maintains context from previous exchanges,
    allowing for follow-up questions and deeper exploration.
    """
    try:
        conv, response_text = conversation_engine.send_message(
            session_id=session_id,
            user_message=request.message,
            max_patterns=request.max_patterns,
            api_key=request.api_key,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Get patterns used in this response
    last_message = conv.messages[-1]
    patterns_used = []
    for pid in last_message.patterns_used:
        pattern = library.get(pid)
        if pattern:
            patterns_used.append(PatternSummary(
                id=pattern.id,
                title=pattern.title,
                domain=pattern.domain,
                era=pattern.era,
            ))
    
    return ConversationResponse(
        session_id=conv.session_id,
        response=response_text,
        patterns_used=patterns_used,
        message_count=len(conv.messages),
    )


@app.get("/conversation/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str):
    """Get the full history of a conversation."""
    conv = conversation_engine.get_conversation(session_id)
    
    if not conv:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    return ConversationHistoryResponse(
        session_id=conv.session_id,
        messages=[
            ConversationMessage(
                role=m.role,
                content=m.content,
                patterns_used=m.patterns_used,
                timestamp=m.timestamp,
            )
            for m in conv.messages
        ],
        created_at=conv.created_at,
    )


@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """Interactive chat UI for conversations."""
    library.load()
    return templates.chat_page(pattern_count=len(library.patterns))


# --- Entry point ---

def run(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()
