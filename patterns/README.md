# Chronicle Pattern Library

This directory contains the curated historical patterns that power Chronicle.

## Pattern Structure

Each pattern is a markdown file with YAML frontmatter:

```markdown
---
id: unique-identifier
title: Human-readable title
domain: technology | economics | governance | social | existential
era: start-end (e.g., 1880-1940)
time_scale: years | decades | centuries | millennia
related: [other-pattern-ids]
confidence: high | medium | low
sources_quality: primary | secondary | synthesized
---

# Title

## Summary
2-3 sentence overview.

## What Happened
Narrative description of the pattern.

## Timeline
Key events with dates.

## Preconditions
What made this possible or likely?

## Contemporary Perspective
What did people living through it think? What did they fear/hope?

## Actual Outcomes
What actually happened? (Short, medium, long term)

## Hindsight
What do we now understand that contemporaries didn't?

## Generalizable Insights
What transfers to other situations?

## Key Differences To Watch
When does this pattern NOT apply?

## Sources
Primary and secondary references.
```

## Domains

- **technology/** - Technological transitions and their effects
- **economics/** - Bubbles, crashes, transformations
- **governance/** - Political and institutional change
- **social/** - Cultural shifts, movements, reforms
- **existential/** - Fears of ending, hopes of transformation

## Quality Standards

1. **Verifiable** - Claims should be traceable to sources
2. **Balanced** - Acknowledge multiple perspectives where they exist
3. **Temporal humility** - Distinguish contemporary views from hindsight
4. **Actionable** - Patterns should yield usable insights
5. **Honest uncertainty** - Flag low confidence areas

## Contributing

Patterns can be added by:
1. Following the template structure
2. Including source citations
3. Flagging contested claims
4. Submitting PR for review

## Current Patterns

| ID | Domain | Era | Title |
|----|--------|-----|-------|
| technological-unemployment-fears | technology | 1800-present | Technological Unemployment Fears |
| printing-press-revolution | technology | 1450-1600 | The Printing Press Revolution |
| year-2000-problem | technology | 1990-2000 | Y2K: The Year 2000 Problem |
| (more to come) | | | |
