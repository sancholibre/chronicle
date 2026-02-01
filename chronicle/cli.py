"""
Chronicle CLI - command line interface for the perspective engine.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

from .patterns import library
from .synthesis import engine, perspective


console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Chronicle: A perspective engine for deep time context."""
    pass


@main.command()
@click.argument("question")
@click.option("--max-patterns", "-n", default=5, help="Maximum patterns to use")
@click.option("--domain", "-d", multiple=True, help="Filter to specific domains")
@click.option("--show-patterns", "-p", is_flag=True, help="Show which patterns were used")
def ask(question: str, max_patterns: int, domain: tuple, show_patterns: bool):
    """Ask a question and get historical perspective."""
    
    console.print()
    console.print("[bold blue]Chronicle is thinking...[/bold blue]")
    console.print()
    
    domains = list(domain) if domain else None
    
    try:
        result = perspective(
            question,
            max_patterns=max_patterns,
            domains=domains,
        )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return
    
    # Display the perspective
    console.print(Panel(
        Markdown(result.synthesis),
        title="[bold green]Historical Perspective[/bold green]",
        border_style="green",
    ))
    
    # Show confidence and caveats
    console.print()
    confidence_color = {
        "high": "green",
        "medium": "yellow",
        "low": "red",
    }.get(result.confidence, "white")
    
    console.print(f"[bold]Confidence:[/bold] [{confidence_color}]{result.confidence}[/{confidence_color}]")
    
    if result.caveats:
        console.print("[bold]Caveats:[/bold]")
        for caveat in result.caveats:
            console.print(f"  • {caveat}")
    
    # Show patterns if requested
    if show_patterns and result.patterns_used:
        console.print()
        console.print("[bold]Patterns used:[/bold]")
        for pattern in result.patterns_used:
            console.print(f"  • {pattern.title} ({pattern.era})")


@main.command()
def list_patterns():
    """List all available patterns."""
    
    patterns = library.all()
    
    if not patterns:
        console.print("[yellow]No patterns loaded.[/yellow]")
        return
    
    table = Table(title="Chronicle Pattern Library")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Domain", style="green")
    table.add_column("Era", style="yellow")
    table.add_column("Confidence", style="blue")
    
    for pattern in sorted(patterns, key=lambda p: (p.domain, p.era)):
        table.add_row(
            pattern.id,
            pattern.title,
            pattern.domain,
            pattern.era,
            pattern.confidence,
        )
    
    console.print(table)


@main.command()
@click.argument("pattern_id")
def show(pattern_id: str):
    """Show details of a specific pattern."""
    
    pattern = library.get(pattern_id)
    
    if not pattern:
        console.print(f"[red]Pattern '{pattern_id}' not found.[/red]")
        return
    
    console.print(Panel(
        Markdown(pattern.content),
        title=f"[bold blue]{pattern.title}[/bold blue]",
        subtitle=f"{pattern.domain} | {pattern.era}",
    ))


@main.command()
@click.argument("query")
def search(query: str):
    """Search patterns by keyword."""
    
    results = library.search_simple(query)
    
    if not results:
        console.print(f"[yellow]No patterns found matching '{query}'[/yellow]")
        return
    
    console.print(f"[bold]Found {len(results)} patterns:[/bold]")
    for pattern in results:
        console.print(f"  • [cyan]{pattern.id}[/cyan]: {pattern.title}")


@main.command()
def domains():
    """List available domains."""
    
    patterns = library.all()
    domain_counts = {}
    
    for pattern in patterns:
        domain_counts[pattern.domain] = domain_counts.get(pattern.domain, 0) + 1
    
    console.print("[bold]Available domains:[/bold]")
    for domain, count in sorted(domain_counts.items()):
        console.print(f"  • {domain}: {count} patterns")


@main.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
@click.option("--port", "-p", default=8000, help="Port to bind to")
def serve(host: str, port: int):
    """Start the HTTP API server."""
    from .api import run
    console.print(f"[bold green]Starting Chronicle API on {host}:{port}[/bold green]")
    console.print(f"[dim]Docs available at http://{host}:{port}/docs[/dim]")
    run(host=host, port=port)


if __name__ == "__main__":
    main()
