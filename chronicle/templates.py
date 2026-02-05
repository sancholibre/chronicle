"""
Chronicle UI Templates - Clean HTML/CSS/JS for human interaction.
"""

BASE_STYLES = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-primary: #0f0f1a;
        --bg-secondary: #1a1a2e;
        --bg-card: #252540;
        --accent: #f39c12;
        --accent-hover: #e67e22;
        --text-primary: #e0e0e0;
        --text-secondary: #888;
        --text-muted: #666;
        --border: #333;
        --success: #27ae60;
        --warning: #f39c12;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
        min-height: 100vh;
        line-height: 1.6;
    }
    
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--accent);
        text-decoration: none;
    }
    
    nav a {
        color: var(--text-secondary);
        text-decoration: none;
        margin-left: 1.5rem;
        transition: color 0.2s;
    }
    
    nav a:hover, nav a.active {
        color: var(--accent);
    }
    
    h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.4rem;
        margin-bottom: 1rem;
        color: var(--text-secondary);
    }
    
    .subtitle {
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Query Section */
    .query-section {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .query-input {
        width: 100%;
        padding: 1rem 1.25rem;
        font-size: 1.1rem;
        background: var(--bg-card);
        border: 2px solid var(--border);
        border-radius: 8px;
        color: var(--text-primary);
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }
    
    .query-input:focus {
        outline: none;
        border-color: var(--accent);
    }
    
    .query-input::placeholder {
        color: var(--text-muted);
    }
    
    .btn {
        display: inline-block;
        padding: 0.8rem 1.5rem;
        background: var(--accent);
        color: var(--bg-primary);
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s, transform 0.2s;
    }
    
    .btn:hover {
        background: var(--accent-hover);
        transform: translateY(-1px);
    }
    
    .btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    .btn-secondary {
        background: transparent;
        border: 2px solid var(--accent);
        color: var(--accent);
    }
    
    .btn-secondary:hover {
        background: rgba(243, 156, 18, 0.1);
    }
    
    /* Results */
    .results-section {
        margin-top: 2rem;
    }
    
    .loading {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
    }
    
    .loading::after {
        content: '';
        animation: dots 1.5s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    
    /* Synthesis Card */
    .synthesis-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        border-left: 4px solid var(--accent);
    }
    
    .synthesis-card h3 {
        color: var(--accent);
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .synthesis-content {
        white-space: pre-wrap;
        line-height: 1.8;
    }
    
    .synthesis-meta {
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .meta-item {
        font-size: 0.9rem;
    }
    
    .meta-label {
        color: var(--text-muted);
    }
    
    /* Pattern Cards */
    .patterns-grid {
        display: grid;
        gap: 1rem;
    }
    
    .pattern-card {
        background: var(--bg-card);
        border-radius: 8px;
        padding: 1.25rem;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        text-decoration: none;
        color: inherit;
        display: block;
    }
    
    .pattern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .pattern-card h4 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .pattern-meta {
        display: flex;
        gap: 1rem;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .domain-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background: rgba(243, 156, 18, 0.2);
        color: var(--accent);
        border-radius: 4px;
        font-size: 0.8rem;
    }
    
    /* Pattern Detail */
    .pattern-detail {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 2rem;
    }
    
    .pattern-detail h1 {
        margin-bottom: 0.5rem;
    }
    
    .pattern-detail .meta {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .pattern-content {
        line-height: 1.8;
    }
    
    .pattern-content h2 {
        color: var(--accent);
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .pattern-content h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .pattern-content p {
        margin-bottom: 1rem;
    }
    
    .pattern-content ul, .pattern-content ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .pattern-content li {
        margin-bottom: 0.5rem;
    }
    
    .pattern-content table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .pattern-content th, .pattern-content td {
        padding: 0.75rem;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }
    
    .pattern-content th {
        color: var(--accent);
    }
    
    /* Domain Filter */
    .domain-filters {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .domain-filter {
        padding: 0.5rem 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }
    
    .domain-filter:hover, .domain-filter.active {
        border-color: var(--accent);
        color: var(--accent);
    }
    
    /* API Key Input */
    .api-key-section {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
    }
    
    .api-key-section summary {
        cursor: pointer;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    .api-key-section input {
        margin-top: 0.5rem;
        width: 100%;
        max-width: 400px;
        padding: 0.5rem 0.75rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 4px;
        color: var(--text-primary);
        font-family: monospace;
    }
    
    /* Error */
    .error {
        background: rgba(231, 76, 60, 0.2);
        border: 1px solid #e74c3c;
        border-radius: 8px;
        padding: 1rem;
        color: #e74c3c;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    footer {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    footer a {
        color: var(--text-secondary);
        text-decoration: none;
    }
    
    footer a:hover {
        color: var(--accent);
    }
    
    /* Responsive */
    @media (max-width: 600px) {
        .container {
            padding: 1rem;
        }
        
        header {
            flex-direction: column;
            gap: 1rem;
        }
        
        nav a {
            margin-left: 0;
            margin-right: 1rem;
        }
        
        .synthesis-meta {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
"""


def app_page(pattern_count: int, domains: dict) -> str:
    """Main interactive app page."""
    domain_buttons = "".join(
        f'<button class="domain-filter" data-domain="{d}">{d} ({c})</button>'
        for d, c in sorted(domains.items())
    )
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronicle - Ask a Question</title>
    <style>{BASE_STYLES}</style>
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">Chronicle</a>
            <nav>
                <a href="/app" class="active">Ask</a>
                <a href="/chat">Chat</a>
                <a href="/browse">Browse Patterns</a>
                <a href="/docs">API</a>
            </nav>
        </header>
        
        <h1>What's on your mind?</h1>
        <p class="subtitle">Describe a situation you're facing, and Chronicle will find historical parallels.</p>
        
        <div class="query-section">
            <input 
                type="text" 
                class="query-input" 
                id="question"
                placeholder="e.g., AI is going to take all the jobs..."
                autofocus
            >
            
            <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                <button class="btn" id="searchBtn" onclick="search()">Find Patterns</button>
                <button class="btn btn-secondary" id="synthesizeBtn" onclick="synthesize()" disabled>
                    Synthesize Perspective
                </button>
            </div>
            
            <details class="api-key-section">
                <summary>🔑 API Key for synthesis (optional)</summary>
                <input 
                    type="password" 
                    id="apiKey" 
                    placeholder="sk-ant-... (Anthropic API key)"
                >
                <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">
                    Synthesis requires an Anthropic API key. Your key is sent directly to Anthropic, not stored.
                </p>
            </details>
        </div>
        
        <div id="results" class="results-section"></div>
        
        <footer>
            <p>
                {pattern_count} patterns across {len(domains)} domains · 
                Built by <a href="https://deaconsantiago.com/willie">Willie 🦣</a>
            </p>
        </footer>
    </div>
    
    <script>
        let foundPatterns = [];
        
        async function search() {{
            const question = document.getElementById('question').value.trim();
            if (!question) return;
            
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<div class="loading">Searching patterns</div>';
            document.getElementById('synthesizeBtn').disabled = true;
            
            try {{
                const res = await fetch('/search?q=' + encodeURIComponent(question));
                foundPatterns = await res.json();
                
                if (foundPatterns.length === 0) {{
                    resultsDiv.innerHTML = '<p style="color: var(--text-secondary);">No matching patterns found. Try different keywords.</p>';
                    return;
                }}
                
                let html = '<h2>Matching Patterns (' + foundPatterns.length + ')</h2>';
                html += '<div class="patterns-grid">';
                
                for (const p of foundPatterns.slice(0, 10)) {{
                    html += `
                        <a href="/browse/${{p.id}}" class="pattern-card">
                            <h4>${{p.title}}</h4>
                            <div class="pattern-meta">
                                <span class="domain-tag">${{p.domain}}</span>
                                <span>${{p.era}}</span>
                            </div>
                        </a>
                    `;
                }}
                
                html += '</div>';
                
                if (foundPatterns.length > 10) {{
                    html += '<p style="margin-top: 1rem; color: var(--text-secondary);">Showing top 10 of ' + foundPatterns.length + ' patterns</p>';
                }}
                
                resultsDiv.innerHTML = html;
                document.getElementById('synthesizeBtn').disabled = false;
                
            }} catch (err) {{
                resultsDiv.innerHTML = '<div class="error">Search failed: ' + err.message + '</div>';
            }}
        }}
        
        async function synthesize() {{
            const question = document.getElementById('question').value.trim();
            const apiKey = document.getElementById('apiKey').value.trim();
            
            if (!question) return;
            
            const resultsDiv = document.getElementById('results');
            const existingResults = resultsDiv.innerHTML;
            
            // Add loading state above patterns
            resultsDiv.innerHTML = '<div class="loading">Synthesizing perspective from historical patterns</div>' + existingResults;
            
            try {{
                const res = await fetch('/perspective', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        question: question,
                        api_key: apiKey || undefined,
                        max_patterns: 5
                    }})
                }});
                
                if (!res.ok) {{
                    const err = await res.json();
                    throw new Error(err.detail || 'Synthesis failed');
                }}
                
                const data = await res.json();
                
                let html = `
                    <div class="synthesis-card">
                        <h3>Historical Perspective</h3>
                        <div class="synthesis-content">${{data.synthesis.replace(/\\n/g, '<br>')}}</div>
                        <div class="synthesis-meta">
                            <div class="meta-item">
                                <span class="meta-label">Confidence:</span> ${{data.confidence}}
                            </div>
                            <div class="meta-item">
                                <span class="meta-label">Patterns used:</span> ${{data.patterns_used.length}}
                            </div>
                        </div>
                    </div>
                `;
                
                // Add pattern cards below synthesis
                html += '<h2>Patterns Referenced</h2><div class="patterns-grid">';
                for (const p of data.patterns_used) {{
                    html += `
                        <a href="/browse/${{p.id}}" class="pattern-card">
                            <h4>${{p.title}}</h4>
                            <div class="pattern-meta">
                                <span class="domain-tag">${{p.domain}}</span>
                                <span>${{p.era}}</span>
                            </div>
                        </a>
                    `;
                }}
                html += '</div>';
                
                resultsDiv.innerHTML = html;
                
            }} catch (err) {{
                // Remove loading, restore patterns
                resultsDiv.innerHTML = '<div class="error">' + err.message + '</div>' + existingResults.replace('<div class="loading">Synthesizing perspective from historical patterns</div>', '');
            }}
        }}
        
        // Enter key triggers search
        document.getElementById('question').addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') search();
        }});
    </script>
</body>
</html>
"""


def browse_page(patterns: list, domains: dict, current_domain: str = None) -> str:
    """Pattern browsing page."""
    domain_buttons = '<button class="domain-filter' + (' active' if not current_domain else '') + '" data-domain="">All</button>'
    domain_buttons += "".join(
        f'<button class="domain-filter{" active" if d == current_domain else ""}" data-domain="{d}">{d} ({c})</button>'
        for d, c in sorted(domains.items())
    )
    
    pattern_cards = ""
    for p in patterns:
        pattern_cards += f"""
            <a href="/browse/{p['id']}" class="pattern-card">
                <h4>{p['title']}</h4>
                <div class="pattern-meta">
                    <span class="domain-tag">{p['domain']}</span>
                    <span>{p['era']}</span>
                </div>
            </a>
        """
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Browse Patterns - Chronicle</title>
    <style>{BASE_STYLES}</style>
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">Chronicle</a>
            <nav>
                <a href="/app">Ask</a>
                <a href="/chat">Chat</a>
                <a href="/browse" class="active">Browse Patterns</a>
                <a href="/docs">API</a>
            </nav>
        </header>
        
        <h1>Pattern Library</h1>
        <p class="subtitle">{len(patterns)} historical patterns across {len(domains)} domains</p>
        
        <div class="domain-filters">
            {domain_buttons}
        </div>
        
        <div class="patterns-grid">
            {pattern_cards}
        </div>
        
        <footer>
            <p>Built by <a href="https://deaconsantiago.com/willie">Willie 🦣</a></p>
        </footer>
    </div>
    
    <script>
        document.querySelectorAll('.domain-filter').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const domain = btn.dataset.domain;
                window.location.href = domain ? '/browse?domain=' + domain : '/browse';
            }});
        }});
    </script>
</body>
</html>
"""


def pattern_detail_page(pattern: dict, content_html: str) -> str:
    """Single pattern detail page."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{pattern['title']} - Chronicle</title>
    <style>{BASE_STYLES}</style>
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">Chronicle</a>
            <nav>
                <a href="/app">Ask</a>
                <a href="/chat">Chat</a>
                <a href="/browse" class="active">Browse Patterns</a>
                <a href="/docs">API</a>
            </nav>
        </header>
        
        <div class="pattern-detail">
            <p style="margin-bottom: 1rem;">
                <a href="/browse" style="color: var(--text-secondary); text-decoration: none;">← Back to patterns</a>
            </p>
            
            <h1>{pattern['title']}</h1>
            
            <div class="meta">
                <span class="domain-tag">{pattern['domain']}</span>
                <span style="color: var(--text-secondary);">{pattern['era']}</span>
                <span style="color: var(--text-secondary);">Time scale: {pattern['time_scale']}</span>
                <span style="color: var(--text-secondary);">Confidence: {pattern['confidence']}</span>
            </div>
            
            <div class="pattern-content">
                {content_html}
            </div>
        </div>
        
        <footer>
            <p>Built by <a href="https://deaconsantiago.com/willie">Willie 🦣</a></p>
        </footer>
    </div>
</body>
</html>
"""


def chat_page(pattern_count: int) -> str:
    """Chat UI for multi-turn conversations."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chronicle - Conversation</title>
    <style>
        {BASE_STYLES}
        
        .chat-container {{
            display: flex;
            flex-direction: column;
            height: calc(100vh - 200px);
            max-height: 700px;
        }}
        
        .messages {{
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 12px 12px 0 0;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .message {{
            max-width: 85%;
            padding: 1rem 1.25rem;
            border-radius: 12px;
            line-height: 1.6;
        }}
        
        .message.user {{
            align-self: flex-end;
            background: var(--accent);
            color: var(--bg-primary);
        }}
        
        .message.assistant {{
            align-self: flex-start;
            background: var(--bg-card);
            border-left: 3px solid var(--accent);
        }}
        
        .message.assistant .content {{
            white-space: pre-wrap;
        }}
        
        .message.assistant .patterns {{
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border);
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        .message.assistant .patterns a {{
            color: var(--accent);
            text-decoration: none;
        }}
        
        .message.assistant .patterns a:hover {{
            text-decoration: underline;
        }}
        
        .message.system {{
            align-self: center;
            background: transparent;
            color: var(--text-muted);
            font-style: italic;
            font-size: 0.9rem;
            padding: 0.5rem;
        }}
        
        .input-area {{
            display: flex;
            gap: 0.75rem;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 0 0 12px 12px;
            border-top: 1px solid var(--border);
        }}
        
        .input-area input {{
            flex: 1;
            padding: 0.875rem 1rem;
            font-size: 1rem;
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
        }}
        
        .input-area input:focus {{
            outline: none;
            border-color: var(--accent);
        }}
        
        .input-area input::placeholder {{
            color: var(--text-muted);
        }}
        
        .input-area button {{
            padding: 0.875rem 1.5rem;
        }}
        
        .typing-indicator {{
            display: flex;
            gap: 4px;
            padding: 1rem 1.25rem;
            background: var(--bg-card);
            border-radius: 12px;
            width: fit-content;
        }}
        
        .typing-indicator span {{
            width: 8px;
            height: 8px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: bounce 1.4s ease-in-out infinite;
        }}
        
        .typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}
        
        @keyframes bounce {{
            0%, 60%, 100% {{ transform: translateY(0); }}
            30% {{ transform: translateY(-6px); }}
        }}
        
        .session-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .session-info {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        
        .new-chat-btn {{
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }}
        
        /* API key toggle */
        .api-toggle {{
            margin-bottom: 1rem;
        }}
        
        .api-toggle summary {{
            cursor: pointer;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .api-toggle input {{
            margin-top: 0.5rem;
            width: 100%;
            max-width: 400px;
            padding: 0.5rem 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-primary);
            font-family: monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="logo">Chronicle</a>
            <nav>
                <a href="/app">Quick Ask</a>
                <a href="/chat" class="active">Chat</a>
                <a href="/browse">Browse Patterns</a>
                <a href="/docs">API</a>
            </nav>
        </header>
        
        <div class="session-controls">
            <span class="session-info" id="sessionInfo">Starting new conversation...</span>
            <button class="btn btn-secondary new-chat-btn" onclick="startNewChat()">New Conversation</button>
        </div>
        
        <details class="api-toggle">
            <summary>🔑 API Key (optional)</summary>
            <input type="password" id="apiKey" placeholder="sk-ant-... (Anthropic API key)">
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">
                Required for responses. Your key is sent directly to Anthropic, not stored.
            </p>
        </details>
        
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message system">
                    Ask me about any situation you're facing, and I'll find historical parallels.
                </div>
            </div>
            
            <div class="input-area">
                <input 
                    type="text" 
                    id="userInput" 
                    placeholder="What's on your mind?"
                    onkeypress="if(event.key === 'Enter') sendMessage()"
                    autofocus
                >
                <button class="btn" onclick="sendMessage()" id="sendBtn">Send</button>
            </div>
        </div>
        
        <footer>
            <p>
                {pattern_count} historical patterns · 
                Built by <a href="https://deaconsantiago.com/willie">Willie 🦣</a>
            </p>
        </footer>
    </div>
    
    <script>
        let sessionId = null;
        
        // Start a conversation on page load
        startNewChat();
        
        async function startNewChat() {{
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '<div class="message system">Starting new conversation...</div>';
            
            try {{
                const res = await fetch('/conversation/start', {{ method: 'POST' }});
                const data = await res.json();
                sessionId = data.session_id;
                
                document.getElementById('sessionInfo').textContent = `Session: ${{sessionId}}`;
                messagesDiv.innerHTML = `<div class="message system">${{data.message}}</div>`;
                document.getElementById('userInput').focus();
                
            }} catch (err) {{
                messagesDiv.innerHTML = `<div class="message system" style="color: #e74c3c;">Failed to start conversation: ${{err.message}}</div>`;
            }}
        }}
        
        async function sendMessage() {{
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            const apiKey = document.getElementById('apiKey').value.trim();
            
            if (!message || !sessionId) return;
            
            const messagesDiv = document.getElementById('messages');
            const sendBtn = document.getElementById('sendBtn');
            
            // Add user message
            messagesDiv.innerHTML += `<div class="message user">${{escapeHtml(message)}}</div>`;
            input.value = '';
            input.disabled = true;
            sendBtn.disabled = true;
            
            // Add typing indicator
            messagesDiv.innerHTML += `<div class="typing-indicator" id="typing"><span></span><span></span><span></span></div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            try {{
                const res = await fetch(`/conversation/${{sessionId}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        message: message,
                        api_key: apiKey || undefined,
                        max_patterns: 5
                    }})
                }});
                
                // Remove typing indicator
                document.getElementById('typing')?.remove();
                
                if (!res.ok) {{
                    const err = await res.json();
                    throw new Error(err.detail || 'Failed to send message');
                }}
                
                const data = await res.json();
                
                // Build assistant message
                let patternsHtml = '';
                if (data.patterns_used && data.patterns_used.length > 0) {{
                    const patternLinks = data.patterns_used.map(p => 
                        `<a href="/browse/${{p.id}}">${{p.title}}</a>`
                    ).join(' · ');
                    patternsHtml = `<div class="patterns">Patterns: ${{patternLinks}}</div>`;
                }}
                
                messagesDiv.innerHTML += `
                    <div class="message assistant">
                        <div class="content">${{formatResponse(data.response)}}</div>
                        ${{patternsHtml}}
                    </div>
                `;
                
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
            }} catch (err) {{
                document.getElementById('typing')?.remove();
                messagesDiv.innerHTML += `<div class="message system" style="color: #e74c3c;">Error: ${{err.message}}</div>`;
            }}
            
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function formatResponse(text) {{
            // Convert markdown-style headers and formatting
            return text
                .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/\\n/g, '<br>');
        }}
    </script>
</body>
</html>
"""
