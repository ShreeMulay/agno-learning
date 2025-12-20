# Example 01: Research Assistant

A web-searching agent that researches topics and provides summarized findings.

## Features

- Web search using DuckDuckGo
- Source citation
- Structured summaries
- Follow-up questions

## Architecture

```
User Query → Research Agent → Web Search Tool → Summarize → Response
```

## Key Concepts

- **Tools**: DuckDuckGoTools for web search
- **Instructions**: Guide the agent to cite sources
- **Structured Output**: Consistent response format

## Run the Example

```bash
python main.py "What are the latest developments in quantum computing?"
```

## Customization Ideas

1. Add multiple search providers
2. Cache search results
3. Add fact-checking step
4. Generate follow-up questions
