"""
Pattern library management - loading, parsing, and indexing historical patterns.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import frontmatter
import yaml


@dataclass
class Pattern:
    """A historical pattern document."""
    
    id: str
    title: str
    domain: str
    era: str
    time_scale: str
    content: str
    raw_markdown: str
    related: list[str] = field(default_factory=list)
    confidence: str = "medium"
    sources_quality: str = "secondary"
    file_path: Optional[Path] = None
    
    # Parsed sections
    summary: str = ""
    what_happened: str = ""
    contemporary_perspective: str = ""
    actual_outcomes: str = ""
    hindsight: str = ""
    generalizable_insights: str = ""
    key_differences: str = ""
    
    @classmethod
    def from_file(cls, path: Path) -> "Pattern":
        """Load a pattern from a markdown file."""
        with open(path, "r") as f:
            post = frontmatter.load(f)
        
        meta = post.metadata
        content = post.content
        
        # Parse sections from content
        sections = parse_sections(content)
        
        return cls(
            id=meta.get("id", path.stem),
            title=meta.get("title", path.stem.replace("-", " ").title()),
            domain=meta.get("domain", "unknown"),
            era=meta.get("era", "unknown"),
            time_scale=meta.get("time_scale", "unknown"),
            content=content,
            raw_markdown=str(post),
            related=meta.get("related", []),
            confidence=meta.get("confidence", "medium"),
            sources_quality=meta.get("sources_quality", "secondary"),
            file_path=path,
            summary=sections.get("summary", ""),
            what_happened=sections.get("what happened", ""),
            contemporary_perspective=sections.get("contemporary perspective", ""),
            actual_outcomes=sections.get("actual outcomes", ""),
            hindsight=sections.get("hindsight", ""),
            generalizable_insights=sections.get("generalizable insights", ""),
            key_differences=sections.get("key differences to watch", ""),
        )
    
    def to_context(self) -> str:
        """Format pattern for inclusion in LLM context."""
        parts = [
            f"# {self.title}",
            f"**Domain:** {self.domain} | **Era:** {self.era} | **Time Scale:** {self.time_scale}",
            "",
        ]
        
        if self.summary:
            parts.extend(["## Summary", self.summary, ""])
        if self.what_happened:
            parts.extend(["## What Happened", self.what_happened, ""])
        if self.contemporary_perspective:
            parts.extend(["## Contemporary Perspective", self.contemporary_perspective, ""])
        if self.actual_outcomes:
            parts.extend(["## Actual Outcomes", self.actual_outcomes, ""])
        if self.hindsight:
            parts.extend(["## Hindsight", self.hindsight, ""])
        if self.generalizable_insights:
            parts.extend(["## Generalizable Insights", self.generalizable_insights, ""])
        if self.key_differences:
            parts.extend(["## Key Differences To Watch", self.key_differences, ""])
        
        return "\n".join(parts)


def parse_sections(content: str) -> dict[str, str]:
    """Parse markdown sections from content."""
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip().lower()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections


class PatternLibrary:
    """Collection of patterns with loading and retrieval."""
    
    def __init__(self, patterns_dir: Optional[Path] = None):
        self.patterns_dir = patterns_dir or Path(__file__).parent.parent / "patterns"
        self.patterns: dict[str, Pattern] = {}
        self._loaded = False
    
    def load(self) -> None:
        """Load all patterns from the patterns directory."""
        if self._loaded:
            return
        
        for domain_dir in self.patterns_dir.iterdir():
            if domain_dir.is_dir() and not domain_dir.name.startswith("."):
                for pattern_file in domain_dir.glob("*.md"):
                    if pattern_file.name == "README.md":
                        continue
                    try:
                        pattern = Pattern.from_file(pattern_file)
                        self.patterns[pattern.id] = pattern
                    except Exception as e:
                        print(f"Warning: Failed to load {pattern_file}: {e}")
        
        self._loaded = True
    
    def get(self, pattern_id: str) -> Optional[Pattern]:
        """Get a pattern by ID."""
        self.load()
        return self.patterns.get(pattern_id)
    
    def all(self) -> list[Pattern]:
        """Get all patterns."""
        self.load()
        return list(self.patterns.values())
    
    def by_domain(self, domain: str) -> list[Pattern]:
        """Get patterns by domain."""
        self.load()
        return [p for p in self.patterns.values() if p.domain == domain]
    
    def search_simple(self, query: str) -> list[Pattern]:
        """Simple keyword search (temporary until embeddings)."""
        self.load()
        
        # Tokenize query into meaningful words
        stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
            'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
            'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
            'because', 'until', 'while', 'about', 'against', 'this', 'that', 'these',
            'those', 'am', 'i', 'me', 'my', 'we', 'our', 'you', 'your', 'it', 'its',
            'what', 'which', 'who', 'whom', 'any', 'both'
        }
        
        # Extract meaningful keywords from query
        words = [w.strip('?.,!').lower() for w in query.split()]
        keywords = [w for w in words if w and len(w) > 2 and w not in stopwords]
        
        if not keywords:
            # Fallback to full query if no keywords extracted
            keywords = [query.lower()]
        
        results = []
        
        for pattern in self.patterns.values():
            score = 0
            title_lower = pattern.title.lower()
            content_lower = pattern.content.lower()
            
            for keyword in keywords:
                # Title matches are worth more
                if keyword in title_lower:
                    score += 15
                # Content matches
                if keyword in content_lower:
                    # Count occurrences for relevance
                    occurrences = content_lower.count(keyword)
                    score += min(occurrences, 10)  # Cap at 10 to avoid one word dominating
                # Related tags
                if any(keyword in tag.lower() for tag in pattern.related):
                    score += 5
                # Domain match
                if keyword in pattern.domain.lower():
                    score += 3
            
            if score > 0:
                results.append((score, pattern))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in results]


# Global library instance
library = PatternLibrary()
