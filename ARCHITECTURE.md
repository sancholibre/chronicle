# Chronicle: Architecture

## Overview

Chronicle is built as **three systems that compose**:

1. **Pattern Library** - Curated historical patterns, indexed for retrieval
2. **Synthesis Engine** - LLM-based reasoning over patterns
3. **Interface Layer** - Human UI + Agent API

```
┌──────────────────────────────────────────────────────────────┐
│                     INTERFACE LAYER                          │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │     Human UI        │  │        Agent API            │   │
│  │  (Conversational)   │  │      (Structured)           │   │
│  └─────────────────────┘  └─────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   SYNTHESIS ENGINE                            │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────────────────┐  │
│  │ Pattern     │ │ Perspective │ │ Calibration            │  │
│  │ Matching    │ │ Synthesis   │ │ & Confidence           │  │
│  └─────────────┘ └─────────────┘ └────────────────────────┘  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                   PATTERN LIBRARY                             │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────────────────┐  │
│  │ Historical  │ │ Pattern     │ │ Source                 │  │
│  │ Events      │ │ Templates   │ │ Documents              │  │
│  └─────────────┘ └─────────────┘ └────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Pattern Library

### What Gets Indexed

Not "all of history." Deliberately curated:

**Pattern Types:**
- **Technological transitions** (agriculture, printing, steam, electricity, computing, internet, AI...)
- **Economic disruptions** (panics, depressions, bubbles, transformations)
- **Social movements** (reforms, revolutions, backlashes)
- **Governance changes** (empire cycles, democracy waves, institutional evolution)
- **Cultural shifts** (enlightenment, romanticism, modernism, postmodernism)
- **Existential concerns** (apocalyptic fears, extinction anxieties, transformation hopes)

**For Each Pattern:**
- **Description** - What happened, when, where
- **Preconditions** - What made it possible/likely
- **Dynamics** - How it unfolded over time
- **Outcomes** - What actually resulted (short, medium, long term)
- **Contemporary perspective** - What people at the time thought
- **Hindsight perspective** - What we now understand differently
- **Analogues** - What other patterns it connects to
- **Sources** - Primary and secondary references

### Data Sources

**Curated First:**
- Our World in Data (quantitative trends)
- Academic history surveys (Cambridge, Oxford series)
- Economic history (Maddison, economic historians)
- Primary source collections (digitized archives)

**Synthesized:**
- Wikipedia as a starting point, verified against primary sources
- Historical databases (CLIO, EH.net)
- Published historical analyses

**NOT included (yet):**
- Comprehensive event databases (too noisy)
- Unverified claims
- Contested narratives without acknowledgment of contestation

### Storage

```
/patterns
  /technology
    printing_revolution.md
    steam_power.md
    electrification.md
    computing_revolution.md
    internet_emergence.md
    ...
  /economics
    tulip_mania.md
    south_sea_bubble.md
    great_depression.md
    ...
  /governance
    fall_of_rome.md
    democracy_waves.md
    ...
```

Each pattern is a structured markdown document:

```markdown
---
id: electrification
domain: technology
era: 1880-1940
time_scale: decades
related: [steam_power, computing_revolution]
confidence: high
---

# Electrification of Industry and Homes

## What Happened
[Narrative description]

## Timeline
- 1880s: Early experiments
- 1890s: First power stations
- ...

## Preconditions
[What made this possible]

## Contemporary Fears
[What people worried about at the time]

## Actual Outcomes
[What actually happened]

## Hindsight
[What we now understand that contemporaries didn't]

## Patterns Worth Noting
[Generalizable insights]

## Sources
[Primary and secondary]
```

### Indexing

Patterns are embedded for semantic search:
- Full document embeddings
- Section-level embeddings (for precise retrieval)
- Tagged metadata for filtering

---

## Layer 2: Synthesis Engine

### Query Processing

1. **Question Analysis**
   - What domain(s) does this touch?
   - What time scale is relevant?
   - What kind of answer is being sought? (prediction, calibration, context, perspective)

2. **Pattern Retrieval**
   - Semantic search across pattern library
   - Filter by domain, era, time_scale
   - Return top-k relevant patterns

3. **Relevance Assessment**
   - For each pattern: how closely does it rhyme?
   - What aspects transfer? What aspects don't?
   - Explicit articulation of similarities AND differences

4. **Synthesis**
   - Weave patterns into coherent narrative
   - Handle contradictions (some patterns suggest X, others Y)
   - Calibrate confidence based on pattern strength

5. **Output Generation**
   - For humans: narrative with explorable depth
   - For agents: structured JSON with claims, confidence, sources

### Prompt Architecture

```
You are Chronicle, a perspective engine that helps people understand 
their current situation in the context of deep time.

Given the user's question and the following historical patterns, 
synthesize a perspective that:
1. Identifies the most relevant historical rhymes
2. Articulates what's similar and what's different about now
3. Describes what actually happened in those historical cases
4. Provides calibrated perspective (how worried/excited should they be?)
5. Offers actionable framing

Important:
- History doesn't repeat, it rhymes. Be precise about what transfers.
- Acknowledge uncertainty. Don't pretend to know what will happen.
- Contemporary observers were often wrong. Hindsight changes things.
- Multiple interpretations of history exist. Note when relevant.
- Your job is perspective, not prediction.

PATTERNS:
{retrieved_patterns}

USER QUESTION:
{question}

PERSPECTIVE:
```

### Calibration Module

Special handling for claims like "this time is different":

```python
def calibrate_novelty(situation, historical_patterns):
    """
    Assess how genuinely novel a situation is vs. 
    how novel it *feels* to people living through it.
    """
    
    # Find closest historical analogues
    analogues = find_analogues(situation, historical_patterns)
    
    # For each: what's the same, what's different?
    similarities, differences = analyze_rhyme(situation, analogues)
    
    # What % of "this time is different" claims were actually right?
    base_rate = get_novelty_base_rate(domain=situation.domain)
    
    # What specific factors suggest genuine novelty?
    novelty_factors = identify_novelty_factors(differences)
    
    return CalibrationResult(
        closest_analogues=analogues,
        similarities=similarities,
        differences=differences,
        base_rate_novel=base_rate,
        novelty_factors=novelty_factors,
        confidence=compute_confidence(...)
    )
```

---

## Layer 3: Interface Layer

### Human UI

**V0: CLI / Chat Interface**
```
$ chronicle "How worried should I be about AI taking my job?"

Chronicle is thinking...

# Historical Perspective

Your concern echoes a pattern we've seen 8 major times since 1800. 
The closest parallel is the 1980s automation fears in manufacturing...

[Continue reading] [Explore patterns] [Ask follow-up]
```

**V1: Web Interface**
- Conversational input
- Collapsible depth (summary → detail → sources)
- Pattern exploration sidebar
- Shareable perspectives

**V2: Integrated**
- Clawdbot skill (Chronicle as a tool I can use)
- Browser extension ("Chronicle this page")
- API for embedding

### Agent API

```typescript
interface ChronicleQuery {
  question: string;
  domains?: string[];        // filter to specific domains
  time_scales?: string[];    // "decade" | "century" | "millennium"
  output_format?: "narrative" | "structured";
  max_patterns?: number;
  include_sources?: boolean;
}

interface ChronicleResponse {
  perspective: {
    summary: string;
    historical_rhymes: HistoricalRhyme[];
    calibration: Calibration;
    actionable_framing: string;
  };
  patterns_used: Pattern[];
  sources: Source[];
  confidence: number;
  caveats: string[];
}

interface HistoricalRhyme {
  pattern_id: string;
  similarity_score: number;
  what_rhymes: string[];
  what_differs: string[];
  what_happened: string;
  contemporary_view: string;
  hindsight_view: string;
}

interface Calibration {
  base_rate_novel: number;    // how often "this time is different" was true
  novelty_factors: string[];  // what actually IS different
  perspective_percentile: number;  // how worried relative to historical norm
}
```

---

## Development Phases

### Phase 0: Foundation (This Week)
- [ ] Project structure
- [ ] First 10 pattern documents (hand-written)
- [ ] Basic RAG pipeline (embed patterns, retrieve, synthesize)
- [ ] CLI interface for testing

### Phase 1: Pattern Library (Next 2 Weeks)
- [ ] 50+ curated patterns across domains
- [ ] Pattern template and quality standards
- [ ] Embedding and retrieval pipeline
- [ ] Source verification workflow

### Phase 2: Synthesis Quality (Weeks 3-4)
- [ ] Prompt engineering for synthesis
- [ ] Calibration module
- [ ] Evaluation dataset (questions + expected insights)
- [ ] Iteration on synthesis quality

### Phase 3: Interfaces (Weeks 5-6)
- [ ] Web UI v0
- [ ] Agent API
- [ ] Clawdbot skill integration

### Phase 4: Iteration (Ongoing)
- [ ] User feedback integration
- [ ] Pattern library expansion
- [ ] Synthesis improvement
- [ ] New domains and time scales

---

## Technology Stack

**Pattern Library:**
- Markdown files in git (versionable, human-editable)
- Embeddings in SQLite + vector extension (simple, portable)

**Synthesis Engine:**
- Python backend
- Claude Sonnet for synthesis (good at nuance)
- Structured output via API

**Interfaces:**
- CLI: Python (Click)
- Web: React + TailwindCSS
- API: FastAPI

**Infrastructure:**
- Start on Railway (simple)
- Git repo for patterns (collaborative editing)

---

## Open Questions

1. **How to handle contested history?** Some events have multiple valid interpretations. How does Chronicle navigate this?

2. **How to avoid hindsight bias?** It's easy to say "they should have known" with 20/20 hindsight. How do we represent what was knowable at the time?

3. **How to keep patterns updated?** History doesn't change, but our understanding does. How does the pattern library evolve?

4. **How to evaluate quality?** What does "good" perspective look like? How do we know if we're getting better?

5. **Where do patterns come from?** Initially hand-curated. Long-term: community contribution? AI-assisted extraction? Academic partnerships?

---

## Next: First Patterns

See /patterns/README.md
