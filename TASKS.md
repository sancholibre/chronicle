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

### In Progress 🔄
- [ ] Test synthesis end-to-end (needs API key)
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

### Patterns to Write
- [ ] **Technology**
  - [ ] Electrification (1880-1940)
  - [ ] Computing Revolution (1950-1990)
  - [ ] Internet Emergence (1990-2010)
  - [ ] Automation Anxiety 1960s
  - [ ] AI Winter(s)
  
- [ ] **Economics**
  - [ ] Tulip Mania
  - [ ] South Sea Bubble
  - [ ] Great Depression
  - [ ] 2008 Financial Crisis
  - [ ] Dot-com Bubble
  
- [ ] **Governance**
  - [ ] Fall of Rome patterns
  - [ ] Democracy waves
  - [ ] Institutional decay
  
- [ ] **Social**
  - [ ] Scientific Revolution
  - [ ] Enlightenment
  - [ ] 1960s social change

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
