# Chronicle: Development Tasks

## Current Sprint: Foundation (Week 1)

### Completed ✅
- [x] Project structure created
- [x] Research document on landscape
- [x] Vision document
- [x] Architecture design
- [x] Pattern format defined
- [x] Initial patterns written:
  - [x] Technological Unemployment Fears
  - [x] Printing Press Revolution  
  - [x] Apocalyptic Predictions
- [x] Pattern loading module
- [x] Basic synthesis engine
- [x] CLI interface
- [x] **10 patterns written** (2026-01-31)
  - [x] Speculative Manias and Crashes (economics)
  - [x] New Era Thinking and Its Failures (economics)
  - [x] Moral Panics and New Media (social)
  - [x] Pandemic Responses Through History (social)
  - [x] Immigration Fears Through History (social)
  - [x] Energy Transitions (technology)
  - [x] Institutional Decay and Renewal (governance)
- [x] Improved keyword search (tokenization, stopwords)
- [x] Better API key handling with multiple sources
- [x] **34 patterns written** (2026-01-31)
  - [x] Health: mental-health-evolution, addiction-waves, germ-theory-resistance, public-health-infrastructure
  - [x] Existential: nuclear-fear-cycles, y2k-and-tech-catastrophism
  - [x] Governance: revolutionary-waves, decolonization-waves
- [x] Deployed to Railway (https://chronicle-production-433c.up.railway.app)

### In Progress 🔄
- [ ] Set up embedding pipeline for semantic search

### Just Added ✅
- [x] HTTP API with FastAPI (2026-01-31)
  - `GET /health`, `/patterns`, `/patterns/{id}`, `/search`, `/domains`
  - `POST /perspective` - main endpoint with BYOK support
  - Interactive docs at `/docs`
  - `chronicle serve` command added

### Blocked ⏸️
- [ ] End-to-end testing blocked on API key configuration

---

## Next Sprint: Pattern Library (Week 2)

### Patterns to Write (remaining gaps)
- [ ] **Technology**
  - [x] Computing Revolution ✅
  - [x] AI Winter(s) ✅
  - [ ] Electrification (1880-1940)
  - [ ] Automation Anxiety 1960s vs today
  
- [ ] **Economics**
  - [x] Speculative Manias (covers Tulip, South Sea, Dot-com, etc.) ✅
  - [x] Great Depression recovery ✅
  - [x] Financial Crises ✅
  - [ ] Currency crises / hyperinflation
  
- [ ] **Governance**
  - [x] Fall of Rome patterns ✅
  - [x] Democracy waves ✅
  - [x] Institutional decay ✅
  - [x] Revolutionary waves ✅
  - [x] Decolonization ✅
  
- [ ] **Social**
  - [x] Scientific Revolution ✅
  - [ ] Enlightenment
  - [ ] Labor movements
  - [ ] Civil rights waves
  
- [ ] **Health**
  - [x] Mental health evolution ✅
  - [x] Addiction waves ✅
  - [x] Germ theory resistance ✅
  - [x] Public health infrastructure ✅
  - [ ] Obesity/metabolic syndrome parallels
  
- [ ] **Existential**
  - [x] Nuclear fear cycles ✅
  - [x] Y2K and tech catastrophism ✅
  - [ ] Asteroid/comet fears
  - [ ] Population bomb predictions

### Infrastructure
- [ ] Set up embedding pipeline (OpenAI or local)
- [ ] Vector storage (sqlite-vec)
- [ ] Semantic search integration
- [ ] Pattern quality scoring

---

## Sprint 3: Synthesis Quality (Weeks 3-4)

- [ ] Evaluation dataset (20+ question/expected-insight pairs)
- [ ] Prompt engineering iteration
- [ ] Calibration module implementation
- [ ] A/B testing framework for prompts
- [ ] Source citation in output

---

## Sprint 4: Interfaces (Weeks 5-6)

- [ ] Web UI v0 (React + Tailwind)
- [ ] Agent API (structured JSON responses)
- [ ] Clawdbot skill integration
- [ ] Shareable perspective URLs

---

## Backlog

### Features
- [ ] Pattern relationships graph
- [ ] "Explore this pattern" drill-down
- [ ] User feedback collection
- [ ] Pattern version history
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Authentication

### Patterns (Long-term)
- [ ] Goal: 100+ patterns across domains
- [ ] Community contribution workflow
- [ ] AI-assisted pattern extraction from sources
- [ ] Academic partnership for verification

### Research
- [ ] How to handle contested history?
- [ ] Evaluation metrics for "good perspective"
- [ ] Calibration benchmarks
- [ ] Temporal reasoning benchmarks

---

## Notes

### Pattern Quality Checklist
Before adding a pattern:
- [ ] Has clear contemporary vs. hindsight distinction
- [ ] Includes source citations
- [ ] Flags contested claims
- [ ] Has generalizable insights
- [ ] Tested with sample queries

### Synthesis Quality Signals
A good perspective should:
- Name specific historical parallels
- Articulate what's the same and different
- Provide calibration (how worried/excited relative to historical norms)
- Acknowledge uncertainty appropriately
- Be actionable (not just interesting)
