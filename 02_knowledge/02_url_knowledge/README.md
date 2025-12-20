# Lesson 02: URL Knowledge

Load content from websites into your agent's knowledge base.

## Concepts Covered

- **URLKnowledge**: Scrape and index web content
- **Web scraping**: Extracting text from HTML
- **Automatic updates**: Refreshing knowledge from live sources
- **Multiple URLs**: Building knowledge from various sources

## How It Works

```python
from agno.agent import Agent
from agno.knowledge.url import URLKnowledge
from agno.vectordb.lancedb import LanceDb

# Create knowledge from URLs
knowledge = URLKnowledge(
    urls=["https://docs.agno.com/introduction"],
    vector_db=LanceDb(
        table_name="web_docs",
        uri="./lancedb",
    ),
)

# Load and index content
knowledge.load()

# Create agent with web knowledge
agent = Agent(
    model=model,
    knowledge=knowledge,
    search_knowledge=True,
)
```

## Use Cases

- Documentation sites
- News articles
- Company knowledge bases
- Product information pages
- Any public web content

## Run the Example

```bash
# Load from Agno docs
python main.py

# Custom URLs
python main.py --urls "https://example.com/page1" "https://example.com/page2"

# Query the knowledge
python main.py --query "How do I create an agent?"
```

## Best Practices

1. **Respect robots.txt**: Don't scrape disallowed pages
2. **Rate limiting**: Don't hammer servers with requests
3. **Cache content**: Avoid re-scraping unchanged content
4. **Clean HTML**: Extract meaningful text only

## Exercises

1. Index a documentation site and build a Q&A agent
2. Create a news aggregator with multiple source URLs
3. Compare answers with and without URL context

## Next Lesson

[03_json_csv_knowledge](../03_json_csv_knowledge/) - Load structured data.
