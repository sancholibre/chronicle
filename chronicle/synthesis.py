"""
Synthesis engine - taking patterns and generating perspective.
"""

import os
from dataclasses import dataclass
from typing import Optional
import anthropic

from .patterns import Pattern, PatternLibrary, library


SYSTEM_PROMPT = """You are Chronicle, a perspective engine that helps people understand their current situation in the context of deep time.

Your role is to:
1. Take a question or concern about the present
2. Connect it to relevant historical patterns
3. Synthesize perspective that is grounded, calibrated, and useful

Guidelines:
- History doesn't repeat, it rhymes. Be precise about what transfers and what doesn't.
- Acknowledge uncertainty. Don't pretend to know what will happen.
- Contemporary observers were often wrong. Distinguish contemporary views from hindsight.
- Multiple interpretations of history exist. Note when relevant.
- Your job is perspective, not prediction.
- Be concrete and specific. Use examples from the patterns provided.
- Surface what's genuinely novel vs. what just feels novel.

Output structure:
1. **Historical Rhymes** - What patterns from history are relevant?
2. **What Actually Happened** - In those historical cases, what was the outcome?
3. **Calibration** - How should the person calibrate their concern/excitement?
4. **What's Different This Time** - Genuine novelty to watch
5. **Perspective Shift** - A reframe that might help

Keep responses focused and actionable. Avoid generic advice."""


@dataclass
class Perspective:
    """A synthesized perspective on a question."""
    
    question: str
    patterns_used: list[Pattern]
    synthesis: str
    confidence: str  # high, medium, low
    caveats: list[str]


class SynthesisEngine:
    """Engine for synthesizing perspective from patterns."""
    
    def __init__(
        self,
        pattern_library: Optional[PatternLibrary] = None,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
    ):
        self.library = pattern_library or library
        self.model = model
        
        # Try to get API key from multiple sources
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            # Check common config locations
            config_paths = [
                os.path.expanduser("~/.anthropic/api_key"),
                os.path.expanduser("~/.config/anthropic/api_key"),
            ]
            for path in config_paths:
                if os.path.exists(path):
                    with open(path) as f:
                        key = f.read().strip()
                    break
        
        if key:
            self.client = anthropic.Anthropic(api_key=key)
        else:
            self.client = None
    
    def generate_perspective(
        self,
        question: str,
        max_patterns: int = 5,
        domains: Optional[list[str]] = None,
    ) -> Perspective:
        """Generate perspective on a question using historical patterns."""
        
        # Check for API client
        if not self.client:
            return Perspective(
                question=question,
                patterns_used=[],
                synthesis="No API key configured. Set ANTHROPIC_API_KEY environment variable "
                         "or create ~/.anthropic/api_key file.",
                confidence="low",
                caveats=["No API key"],
            )
        
        # Find relevant patterns
        patterns = self._find_relevant_patterns(question, max_patterns, domains)
        
        if not patterns:
            return Perspective(
                question=question,
                patterns_used=[],
                synthesis="I don't have relevant historical patterns for this question yet. "
                         "The pattern library is still growing.",
                confidence="low",
                caveats=["No patterns available"],
            )
        
        # Build context from patterns
        patterns_context = "\n\n---\n\n".join(p.to_context() for p in patterns)
        
        # Generate synthesis
        user_prompt = f"""HISTORICAL PATTERNS:
{patterns_context}

---

USER QUESTION:
{question}

Please provide a perspective on this question, drawing on the historical patterns above. 
Be specific about which patterns apply and how. Acknowledge what's different about the current situation."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        
        synthesis = response.content[0].text
        
        # Assess confidence based on pattern quality
        confidence = self._assess_confidence(patterns, question)
        
        # Generate caveats
        caveats = self._generate_caveats(patterns)
        
        return Perspective(
            question=question,
            patterns_used=patterns,
            synthesis=synthesis,
            confidence=confidence,
            caveats=caveats,
        )
    
    def _find_relevant_patterns(
        self,
        question: str,
        max_patterns: int,
        domains: Optional[list[str]],
    ) -> list[Pattern]:
        """Find patterns relevant to a question."""
        # Simple search for now - will upgrade to embeddings
        all_patterns = self.library.search_simple(question)
        
        if domains:
            all_patterns = [p for p in all_patterns if p.domain in domains]
        
        return all_patterns[:max_patterns]
    
    def _assess_confidence(self, patterns: list[Pattern], question: str) -> str:
        """Assess confidence in the perspective."""
        if not patterns:
            return "low"
        
        # Check pattern confidence levels
        confidences = [p.confidence for p in patterns]
        
        if all(c == "high" for c in confidences) and len(patterns) >= 3:
            return "high"
        elif any(c == "high" for c in confidences):
            return "medium"
        else:
            return "low"
    
    def _generate_caveats(self, patterns: list[Pattern]) -> list[str]:
        """Generate caveats about the perspective."""
        caveats = []
        
        if len(patterns) < 3:
            caveats.append("Based on limited pattern matches")
        
        if any(p.sources_quality == "synthesized" for p in patterns):
            caveats.append("Some patterns based on synthesized sources")
        
        if any(p.confidence == "low" for p in patterns):
            caveats.append("Some patterns have low confidence ratings")
        
        return caveats


# Default engine instance
engine = SynthesisEngine()


def perspective(question: str, **kwargs) -> Perspective:
    """Convenience function for getting perspective."""
    return engine.generate_perspective(question, **kwargs)
