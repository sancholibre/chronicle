# Chronicle

**A perspective engine for deep time context.**

Chronicle helps you understand your current situation in the context of human history. You bring a question; Chronicle finds historical patterns, synthesizes perspective, and helps you calibrate your concerns.

## The Idea

Every major moment feels unprecedented to those living through it. But most "unprecedented" situations rhyme with something from the past. Chronicle surfaces those rhymes—not to predict the future, but to provide perspective.

**Not:** "Here's what will happen."  
**Instead:** "Here's what happened before in similar situations. Here's what was the same and different. Here's how people at the time thought about it, and what we now understand they missed."

## Quick Start

```bash
# Install
pip install -e .

# Configure API key (required for synthesis)
export ANTHROPIC_API_KEY="your-key-here"
# Or: echo "your-key" > ~/.anthropic/api_key

# Ask a question
chronicle ask "How worried should I be about AI taking my job?"

# List available patterns
chronicle list-patterns

# Search patterns
chronicle search "technology unemployment"

# Show a specific pattern
chronicle show technological-unemployment-fears
```

## Example

```
$ chronicle ask "Is this AI hype cycle going to crash like crypto?"

Chronicle is thinking...

┌──────────────────────────────────────────────────────────────────────────────┐
│                          Historical Perspective                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ **Historical Rhymes**                                                         │
│                                                                               │
│ Your question echoes a pattern we've seen with every major technology...     │
│ [continued synthesis]                                                         │
└──────────────────────────────────────────────────────────────────────────────┘

Confidence: medium
Caveats:
  • Based on limited pattern matches
```

## How It Works

1. **Pattern Library** - Curated historical patterns (technological transitions, economic disruptions, social movements, etc.)
2. **Pattern Matching** - Given your question, find relevant historical rhymes
3. **Synthesis Engine** - Weave patterns into coherent perspective using LLM reasoning
4. **Calibration** - Help you understand what's genuinely novel vs. what just feels novel

## Pattern Library

Patterns are organized by domain:

- `technology/` - Technological transitions and their effects
- `economics/` - Bubbles, crashes, transformations
- `governance/` - Political and institutional change
- `social/` - Cultural shifts, movements, reforms
- `existential/` - Fears of ending, hopes of transformation

Each pattern includes:
- What happened
- Contemporary perspective (what people at the time thought)
- Actual outcomes (what resulted)
- Hindsight (what we now understand they missed)
- Generalizable insights

See [patterns/README.md](patterns/README.md) for the full structure.

## Design Philosophy

1. **Query-driven, not browse-driven** - You come with a question, you leave with perspective
2. **Synthesis over retrieval** - Connect patterns, don't just fetch facts
3. **Calibrated confidence** - Know when something genuinely IS different
4. **Temporal humility** - History is contested; we acknowledge uncertainty
5. **Agent-native** - Built for machine reasoning, human UI on top

## HTTP API (for Agents)

Start the server:
```bash
chronicle serve --port 8000
```

Interactive docs at `http://localhost:8000/docs`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/patterns` | List all patterns |
| GET | `/patterns/{id}` | Get specific pattern |
| GET | `/search?q=...` | Search patterns |
| GET | `/domains` | List domains |
| POST | `/perspective` | **Main endpoint** - get historical perspective |

### Agent Example

```python
import requests

resp = requests.post("http://localhost:8000/perspective", json={
    "question": "Is the current AI hype a bubble?",
    "api_key": "sk-..."  # BYOK, or set ANTHROPIC_API_KEY env var
})
print(resp.json()["synthesis"])
```

## Project Status

Chronicle is in early development. Current state:

- [x] Project structure
- [x] Pattern format and loading
- [x] Basic synthesis engine
- [x] CLI interface
- [x] HTTP API for agents
- [x] 10 patterns across 5 domains
- [ ] Embedding-based retrieval
- [ ] Web interface
- [ ] More patterns (goal: 50+)

## Contributing Patterns

Patterns are markdown files with YAML frontmatter. See the existing patterns for format. Key requirements:

1. Include source citations
2. Distinguish contemporary views from hindsight
3. Flag contested claims
4. Focus on generalizable insights

## Why "Chronicle"?

A chronicle is a record of events in time order. Chronicle (the tool) helps you see your present moment as part of that ongoing record—connected to what came before, informing what comes next.

---

*Built by Willie 🦣 with Deacon.*
