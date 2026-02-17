"""
Chronicle HTTP API - Simple REST endpoint for agents and applications.
"""

import os
import time
import markdown
from typing import Optional
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .patterns import library
from .synthesis import SynthesisEngine, Perspective
from .conversations import ConversationEngine, conversation_engine


# --- Error Handling ---
def sanitize_error(e: Exception) -> str:
    """Sanitize error messages to avoid leaking internals."""
    error_str = str(e).lower()
    # Don't leak API key errors or internal details
    if "api_key" in error_str or "api key" in error_str:
        return "API configuration error. Please try again or use your own API key."
    if "rate" in error_str and "limit" in error_str:
        return "Rate limit exceeded. Please wait and try again."
    if "timeout" in error_str:
        return "Request timed out. Please try again."
    # Generic error for anything else
    return "An error occurred while processing your request. Please try again."


# --- Demo Mode Rate Limiting ---
# Simple in-memory rate limiter: 5 queries per IP per day
DEMO_RATE_LIMIT = 5
demo_usage: dict[str, list[float]] = defaultdict(list)

def check_demo_rate_limit(ip: str) -> tuple[bool, int]:
    """Check if IP can use demo mode. Returns (allowed, remaining)."""
    now = time.time()
    day_ago = now - 86400
    
    # Clean old entries
    demo_usage[ip] = [t for t in demo_usage[ip] if t > day_ago]
    
    remaining = DEMO_RATE_LIMIT - len(demo_usage[ip])
    return remaining > 0, max(0, remaining)

def record_demo_usage(ip: str):
    """Record a demo query for rate limiting."""
    demo_usage[ip].append(time.time())


# --- Pre-generated Examples ---
DEMO_EXAMPLES = {
    "Is AI hype like the dotcom bubble?": {
        "synthesis": """**Historical Rhymes**

The current AI moment echoes several historical technology cycles:

1. **Internet Hype Cycles (1994-2000)**: Massive investment based on transformative potential, with valuations detached from current revenue. Many comparisons are apt—the "this changes everything" rhetoric, the flood of startups, the infrastructure buildout preceding clear use cases.

2. **Computing Revolution (1950s-1980s)**: Early predictions ranged from "computers will only be useful for census data" to "artificial intelligence is 20 years away" (said repeatedly for 60 years). The technology was transformative, but timelines were wildly wrong.

3. **Electrification (1880s-1920s)**: Took 40+ years from invention to widespread productivity gains. Factory owners initially just replaced steam engines with electric motors; the real gains came from redesigning workflows around electricity's flexibility.

**What Actually Happened**

In the dotcom crash, ~80% of internet companies failed, but the survivors (Amazon, Google, eBay) became among the most valuable companies in history. The technology thesis was correct; the valuations were premature. The Nasdaq took 15 years to recover its 2000 peak.

**Calibration**

The "bubble" framing may be too binary. Questions to consider:
- Dotcom bubble: overvaluation of *applications* before infrastructure existed
- AI today: infrastructure (compute, models) exists; applications are emerging
- Key difference: AI companies like NVIDIA are profitable; many dotcom companies had no revenue

Historical base rate: transformative technologies usually take 2-3x longer than predicted but go 10x further than imagined.

**What's Different This Time**

- AI produces working outputs immediately (generative AI), unlike early internet "portals"
- Major tech companies are profitable and funding development, not VC-dependent startups
- The technology is improving on a steep curve, not waiting for infrastructure buildout

**Perspective Shift**

Rather than "is this a bubble?", ask "what's the timeline mismatch?" The dotcom crash wasn't wrong about the internet—it was wrong about timing. If AI follows similar patterns, current valuations might be 5-10 years premature, but the directional bet could still be correct.""",
        "confidence": "medium-high",
        "patterns_used": ["internet-hype", "computing-revolution", "electrification"]
    },
    "Is this the most polarized America has ever been?": {
        "synthesis": """**Historical Rhymes**

American political polarization has several historical precedents that exceed current levels:

1. **Civil War Era (1850s-1860s)**: Congressmen literally beat each other on the floor. Preston Brooks caned Charles Sumner nearly to death in the Senate chamber. The country then fought a war that killed 2% of the population.

2. **Reconstruction and Redemption (1865-1877)**: Organized political violence, thousands of Black Americans murdered for voting, entire state governments overthrown by force.

3. **1960s-1970s**: Political assassinations (JFK, RFK, MLK, Malcolm X), domestic terrorism (over 2,500 bombings in 1971-1972 alone), National Guard shooting students, cities burning.

4. **1920s-1930s**: KKK had 4-6 million members, open Nazi rallies in Madison Square Garden, violent labor conflicts, Business Plot to overthrow FDR.

**What Actually Happened**

In each case, the country did not permanently fracture (with the temporary exception of the Civil War). Periods of extreme polarization were followed by periods of relative consensus—though often through suppression of legitimate grievances rather than resolution.

**Calibration**

Current polarization is historically notable but not unprecedented. Key metrics:
- Political violence: significantly lower than 1960s-70s
- Congressional bipartisanship: at historic lows since ~2010
- Media environment: unprecedented fragmentation (genuinely new)
- Geographic sorting: historically high

You're likely experiencing recency bias amplified by social media's visibility of conflict.

**What's Different This Time**

- Information environment is genuinely unprecedented (algorithmic amplification, filter bubbles)
- Decline of shared information sources (no more "Walter Cronkite moment")
- Economic anxiety hitting demographics (white non-college) previously insulated from it
- Both parties increasingly view the other as existential threat

**Perspective Shift**

The question isn't whether polarization is unprecedented (it isn't), but whether the *mechanisms* of polarization are new enough to produce different outcomes. The media environment is the wild card that doesn't have a clean historical parallel.""",
        "confidence": "high",
        "patterns_used": ["civil-rights-waves", "democracy-waves", "generational-conflicts"]
    },
    "Will AI take all the jobs?": {
        "synthesis": """**Historical Rhymes**

Technological unemployment fears have recurred with every major innovation:

1. **Luddites (1811-1816)**: Textile workers destroyed machines, fearing permanent unemployment. Textile employment actually *increased* as lower prices expanded demand, though individual craftsmen were displaced.

2. **Automation Anxiety (1950s-1960s)**: "Automation will create unemployment the likes of which we have never seen" (JFK, 1960). Instead, employment shifted to services; manufacturing output grew while manufacturing *employment share* fell.

3. **ATMs and Bank Tellers**: Predicted to eliminate teller jobs. Instead, cheaper branch operation led to more branches, and tellers shifted to relationship/sales roles. Teller employment grew until 2000.

4. **Agricultural Mechanization**: US farm employment fell from 40% (1900) to 2% (today). This was traumatic for individuals but occurred over generations, allowing adaptation.

**What Actually Happened**

Across 200+ years of technological disruption:
- Short-term displacement is real and painful for affected workers
- Long-term total employment has always recovered and grown
- New job categories emerged that were unimaginable before (social media manager, data scientist, UX designer)
- Transition periods vary from years to decades

**Calibration**

Historical base rate: technology destroys specific jobs while creating new categories. But:
- Speed of transition matters enormously for human welfare
- "Long run we're all fine" is cold comfort to a 55-year-old whose skills are obsolete
- Some transitions were brutal (Great Depression was partly agricultural transition)

The correct question isn't "will jobs exist?" but "how fast is the transition, and who bears the costs?"

**What's Different This Time**

- AI targets cognitive work, not just physical labor (historically safer)
- Speed of capability improvement is faster than previous technologies
- General-purpose nature means multiple job categories affected simultaneously
- Unlike past automation, this might compete on "human" qualities (creativity, communication)

**Perspective Shift**

Rather than "jobs vs. no jobs," think about "tasks within jobs." Most jobs are bundles of tasks; AI will automate some tasks while changing which human tasks are valuable. The historical pattern suggests more jobs, but potentially very different jobs—and a transition period that policy choices will make either manageable or brutal.""",
        "confidence": "medium",
        "patterns_used": ["technological-unemployment-fears", "productivity-paradox", "labor-movements"]
    }
}
from . import templates


# --- Models ---

class PerspectiveRequest(BaseModel):
    """Request for historical perspective."""
    question: str
    max_patterns: int = 5
    domains: Optional[list[str]] = None
    api_key: Optional[str] = None  # BYOK support
    demo: bool = False  # Demo mode - rate limited, no key required


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
            <a href="/app">Try It — Ask a Question</a>
            <a href="/browse" class="secondary">Browse Patterns</a>
            <a href="/docs" class="secondary">API Docs</a>
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
async def get_perspective(request: PerspectiveRequest, http_request: Request):
    """
    Get historical perspective on a question.
    
    This is the main endpoint. Provide a question about your current situation,
    and Chronicle will find relevant historical patterns and synthesize perspective.
    
    Modes:
    - BYOK: Pass your own api_key
    - Demo: Set demo=true for rate-limited free access (5/day)
    - Server: Uses ANTHROPIC_API_KEY env var if set
    """
    # Check for pre-generated example (instant response, no rate limit)
    if request.question in DEMO_EXAMPLES:
        ex = DEMO_EXAMPLES[request.question]
        return PerspectiveResponse(
            question=request.question,
            synthesis=ex["synthesis"],
            confidence=ex["confidence"],
            caveats=["This is a pre-generated example response."],
            patterns_used=[
                PatternSummary(id=pid, title=pid.replace("-", " ").title(), domain="cached", era="")
                for pid in ex["patterns_used"]
            ],
        )
    
    # Determine API key to use
    api_key = request.api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    # If no user key and demo mode requested
    if not request.api_key and request.demo:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise HTTPException(
                status_code=503,
                detail="Demo mode unavailable - server not configured."
            )
        
        # Rate limit check
        client_ip = http_request.client.host if http_request.client else "unknown"
        allowed, remaining = check_demo_rate_limit(client_ip)
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail="Demo rate limit exceeded (5/day). Use your own API key for unlimited access."
            )
        
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        record_demo_usage(client_ip)
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Use demo=true for free trial, or provide your own api_key."
        )
    
    # Create engine with appropriate key
    engine = SynthesisEngine(api_key=api_key)
    
    try:
        result = engine.generate_perspective(
            question=request.question,
            max_patterns=request.max_patterns,
            domains=request.domains,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=sanitize_error(e))
    
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
    request: Request,
    q: str = Query(..., description="Your question about the current situation"),
    patterns: int = Query(5, ge=1, le=10, description="Max patterns to consider"),
    api_key: Optional[str] = Query(None, description="Anthropic API key (BYOK)"),
    demo: bool = Query(False, description="Use demo mode (rate limited, no key required)"),
):
    """
    Simple GET endpoint for quick queries.
    
    Example: /ask?q=Is AI hype like the dotcom bubble?
    
    Returns plain text synthesis for easy consumption.
    
    Modes:
    - BYOK: Pass your own api_key
    - Demo: Set demo=true for rate-limited free access (5/day)
    - Server: Uses ANTHROPIC_API_KEY env var if set
    """
    # Check for pre-generated example (instant response, no rate limit)
    if q in DEMO_EXAMPLES:
        ex = DEMO_EXAMPLES[q]
        return {
            "question": q,
            "synthesis": ex["synthesis"],
            "confidence": ex["confidence"],
            "patterns": ex["patterns_used"],
            "demo_mode": True,
            "cached": True,
        }
    
    # Determine API key to use
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    is_demo_mode = False
    
    # If no user key, check demo mode
    if not api_key and demo:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise HTTPException(
                status_code=503,
                detail="Demo mode unavailable - server not configured."
            )
        
        # Rate limit check
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining = check_demo_rate_limit(client_ip)
        
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail=f"Demo rate limit exceeded. Try again tomorrow or use your own API key."
            )
        
        key = os.environ.get("ANTHROPIC_API_KEY")
        is_demo_mode = True
        record_demo_usage(client_ip)
    
    if not key:
        raise HTTPException(
            status_code=401, 
            detail="API key required. Pass ?api_key=YOUR_KEY, use demo=true for free trial, or set ANTHROPIC_API_KEY env var."
        )
    
    engine = SynthesisEngine(api_key=key)
    
    try:
        result = engine.generate_perspective(question=q, max_patterns=patterns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=sanitize_error(e))
    
    # Return structured but simple response
    response = {
        "question": result.question,
        "synthesis": result.synthesis,
        "confidence": result.confidence,
        "patterns": [p.title for p in result.patterns_used],
    }
    
    if is_demo_mode:
        client_ip = request.client.host if request.client else "unknown"
        _, remaining = check_demo_rate_limit(client_ip)
        response["demo_mode"] = True
        response["demo_queries_remaining"] = remaining
    
    return response


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
        raise HTTPException(status_code=500, detail=sanitize_error(e))
    
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
        raise HTTPException(status_code=500, detail=sanitize_error(e))
    
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
