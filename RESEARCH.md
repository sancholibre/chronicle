# Chronicle: Research & Landscape Analysis

## What Exists

### 1. Long Now Foundation
- **What:** Cultural institution promoting 10,000-year thinking. 10,000-year clock project.
- **Approach:** Philosophical, artistic, advocacy-based
- **Limitation:** Not a tool. No interactive intelligence. Inspires but doesn't assist.

### 2. Our World in Data (OWID)
- **What:** Research publication with interactive charts on global problems
- **Approach:** Data journalism, static visualizations, long-term trends
- **Strengths:** Excellent data, trusted source, beautiful charts
- **Limitation:** Passive. You browse topics; it doesn't answer YOUR question. No synthesis.

### 3. Gapminder
- **What:** Educational tool fighting systematic misconceptions
- **Approach:** Interactive bubble charts, ignorance surveys
- **Limitation:** Focused on correcting specific misconceptions, not providing perspective on novel questions.

### 4. Big History Project (David Christian / Gates)
- **What:** Academic discipline + curriculum from Big Bang to present
- **Approach:** Educational, narrative-driven, 13.8 billion year scope
- **Limitation:** It's a course, not a tool. You learn the framework; you can't query it.

### 5. Histography.io
- **What:** Beautiful interactive timeline of Wikipedia events
- **Approach:** Visual exploration, every dot is an event
- **Limitation:** Pure visualization. No intelligence. No synthesis. No "so what."

### 6. ChronoZoom (Microsoft Research)
- **What:** Zoomable timeline from Big Bang to present
- **Status:** Defunct/abandoned
- **Why it failed:** Maintenance burden, no clear use case beyond "cool demo," no sustainable business model

### 7. Wait But Why
- **What:** Tim Urban's essays including deep time perspectives
- **Approach:** Brilliant narrative synthesis (e.g., "Die Progress Units")
- **Limitation:** Static content. One author's takes. Not queryable.

### 8. Historical Data on GitHub
- **What:** Mostly financial/market data APIs
- **Approach:** Raw data access for backtesting, analysis
- **Limitation:** Narrow domains (stocks, crypto). No synthesis layer.

---

## The Gap

Every existing tool shares the same fundamental limitation:

**They are PASSIVE. You explore THEIR structure. They don't answer YOUR question.**

None of them:
- Take your specific situation and find historical rhymes
- Synthesize perspective across multiple time scales
- Reason about patterns rather than just display data
- Serve as an intelligence layer for decision-making
- Build capability that agents can use for broad reasoning

---

## What Failed and Why

| Project | Failure Mode |
|---------|--------------|
| ChronoZoom | Cool demo, no use case. Who comes back daily? |
| Various timeline tools | One-time builds, no iteration, maintenance burden |
| "All of history" visualizations | Too broad to be useful for anything specific |
| Historical AI chatbots | Shallow retrieval, no genuine synthesis |

**Common failure pattern:** Build impressive visualization → no clear "job to be done" → usage drops → project abandoned.

The successful ones (OWID, Gapminder) survived because they serve a clear purpose: **fighting misconceptions with data for journalists, educators, policymakers.**

---

## What Would Be New

### Chronicle: An AI that reasons across time

Not a visualization. Not a database. An **intelligence layer** that:

1. **Takes your question** → "How worried should I be about AI unemployment?"
2. **Finds historical patterns** → Previous technological unemployment fears, actual outcomes, what was different, what rhymes
3. **Synthesizes perspective** → Not just facts but *wisdom*: "Here's how this compares to 47 similar transitions. Here's what actually happened. Here's what was different then vs now."
4. **Provides calibration** → "Your anxiety level matches 34% of Americans during the Cold War. Most of them were fine. Here's what they wish they'd known."

### The Key Insight

Everyone builds **data first, query later.**

Chronicle should be **query first, data in service of perspective.**

The question isn't "how do we store all of history?" It's "how do we help someone see their situation in the context of deep time?"

---

## What Comes After Chronicle

If we build the synthesis layer well, others could build:

### For Humans
- **Decision support tools** with "historical due diligence"
- **Journalism tools** ("how does this compare to...")
- **Therapy/coaching tools** ("humans have faced this before...")
- **Investment/risk tools** ("this pattern looks like...")
- **Education tools** ("understand this event in context")

### For Agents
- **Broad contextual reasoning** - agents that don't just retrieve but synthesize
- **Wisdom accumulation** - knowledge that compounds, not just stacks
- **Calibration capability** - knowing when something is actually novel vs pattern
- **Perspective shifting** - zooming between time scales deliberately

### For the Ecosystem
- A new kind of RAG that indexes **patterns** not just facts
- Training data for "wise" agents
- Benchmarks for cross-temporal reasoning
- Open infrastructure others can build on

---

## Design Principles (Emerging)

1. **Query-driven, not browse-driven** - You come with a question, you leave with perspective
2. **Synthesis over retrieval** - Connect patterns, don't just fetch facts
3. **Calibrated confidence** - Know when something genuinely IS different
4. **Multi-scale fluency** - Move between centuries and decades naturally
5. **Agent-native** - Build for machine reasoning, add human UI on top
6. **Sustainable** - Clear use case, clear value, people come back

---

## Next: What is the product?

See VISION.md
