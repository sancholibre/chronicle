# Chronicle: Vision Document

## The Core Idea

**Chronicle is a perspective engine.** 

You bring a question, concern, or situation. Chronicle places it in the context of deep time—finding patterns, precedents, and perspective across human history—and returns not just information but *wisdom*.

---

## The Name

"Chronicle" suggests:
- Recording events across time (a chronicle)
- The ongoing human narrative
- A companion that knows the story

It's simple, memorable, and gets out of the way of the experience.

---

## Who Is This For?

### Primary: Decision-makers facing uncertainty
- Founders wondering if their market will exist
- Investors evaluating novel risks
- Leaders navigating unprecedented situations
- Anyone asking "is this really different this time?"

### Secondary: Curious minds seeking context
- Writers researching topics
- Students understanding events
- Anyone who reads Wait But Why and wishes they could query it

### Tertiary (and secretly primary): Agents
- AI systems that need to reason broadly, not just retrieve narrowly
- The infrastructure layer for "wise" AI

---

## The Experience (Human)

### You arrive with a question:
> "How worried should I be about AI taking my software engineering job?"

### Chronicle responds with perspective:

**Historical Rhymes**
- "Technological unemployment" fear has occurred 8 major times since 1800
- Closest parallel: 1980s automation fears in manufacturing
- Key differences from previous transitions: [speed, scope, nature of displaced skills]

**What Actually Happened**
- In 7/8 cases, new jobs emerged faster than old ones disappeared
- The 1 exception (Great Depression-era agriculture) had specific conditions
- Transition periods averaged 15-20 years of genuine disruption

**Calibration**
- Your concern level matches ~40th percentile of historical "this time is different" claims
- 60% of concerns at this level resolved positively within a decade
- The 40% that didn't: here's what made them different

**Perspective Shift**
- If you were asking this question in 1995 about the internet...
- If you were asking this in 1920 about electrification...
- What did people wish they'd done differently?

**What To Do With This**
- Historical patterns suggest: [specific actionable framing]
- Areas where this actually IS different to monitor: [genuine novelty]
- The question behind your question might be: [reframe]

---

## The Experience (Agent)

Agents query Chronicle as an API/tool:

```
chronicle.perspective(
  question="Will cryptocurrency replace traditional banking?",
  time_scales=["decade", "century", "millennium"],
  domains=["finance", "technology", "governance"],
  output="structured"
)
```

Returns structured analysis that the agent can use for:
- Calibrating claims ("this is genuinely novel" vs "we've seen this before")
- Providing context in conversations
- Making decisions with historical grounding
- Avoiding recency bias and temporal provincialism

---

## What Chronicle Is NOT

- **Not a search engine** - You don't browse; you ask and receive
- **Not a timeline visualization** - No zoomable UIs (that's been done, it failed)
- **Not a history textbook** - Not comprehensive; deliberately selective for relevance
- **Not a prediction engine** - "Here's what happened before" ≠ "Here's what will happen"
- **Not infallible** - Calibrated uncertainty is a feature, not a bug

---

## The Architecture (High Level)

### Layer 1: Knowledge Substrate
- Curated historical patterns, not comprehensive facts
- Indexed by pattern type, time scale, domain
- Sources: academic history, OWID data, primary sources, synthesized narratives

### Layer 2: Pattern Matching Engine  
- Given a question, find relevant historical patterns
- Not keyword matching—semantic pattern recognition
- "What kind of situation is this?" → "We've seen situations like this before"

### Layer 3: Synthesis Engine
- Weave patterns into coherent perspective
- Handle contradictions and edge cases
- Produce calibrated, nuanced output

### Layer 4: Interface Layer
- Human UI: conversational, explorable
- Agent API: structured, queryable
- Both get the same underlying intelligence

---

## What Makes This Hard

1. **Avoiding false pattern matching** - History doesn't repeat, it rhymes. Getting the rhyme detection right is hard.

2. **Calibration** - Knowing when something IS genuinely novel vs. just feeling novel.

3. **Avoiding hindsight bias** - Easy to say "they should have known" with 20/20 hindsight.

4. **Scope** - Can't index all of history. What patterns are worth encoding?

5. **Epistemic humility** - History is contested. Multiple interpretations exist.

---

## What Makes This Possible Now

1. **LLMs can synthesize** - Previous attempts were limited to retrieval. Now we can actually reason across sources.

2. **RAG patterns exist** - We know how to ground generation in sources.

3. **Agent ecosystem emerging** - There's demand for this capability in AI systems.

4. **Curated data available** - OWID, academic sources, digitized archives.

5. **The moment is right** - People feel unmoored from history. They want perspective.

---

## Success Metrics

### For Humans
- Do people feel more grounded after using Chronicle?
- Do they make different (better?) decisions?
- Do they return?

### For Agents
- Does Chronicle improve agent reasoning on novel situations?
- Do agents using Chronicle make fewer recency-biased errors?
- Is the API actually used in production systems?

### For the Project
- Is the pattern library growing and improving?
- Are we learning what patterns matter?
- Is the synthesis quality improving with use?

---

## The Bet

The bet is: **perspective is a product.**

People will pay (with time, attention, or money) for calibrated, historical perspective on their current situation.

If we're right, Chronicle becomes infrastructure for wise decision-making—both human and machine.

If we're wrong, we've at least built something interesting that scratches a genuine itch.

---

## Next: Architecture

See ARCHITECTURE.md
