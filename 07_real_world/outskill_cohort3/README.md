# Outskill GenAI Engineering Cohort 3 - Week 12 Examples

Examples adapted from [Outskill GenAI Engineering Cohort 3](https://github.com/outskill-git/GenAIEngineering-Cohort3) Week 12 materials, converted for the Agno framework.

## Examples

| Example | Description | Key Pattern |
|---------|-------------|-------------|
| `movie_script_generator` | Generate movie scripts with structured Pydantic output | Structured Output |
| `csv_data_analyst` | Analyze CSV files using SQL queries | CsvTools |
| `eda_visualization_agent` | Create data visualizations and charts | PythonTools |
| `code_to_diagram` | Generate UML diagrams from code | FileTools |
| `reasoning_agent` | Solve logic puzzles with reasoning mode | Reasoning |
| `web_search_agent` | Search the web with DuckDuckGo | DuckDuckGo Tool |
| `finance_agent` | Get stock data and analyst recommendations | YFinance Tools |
| `agent_team` | Combine multiple agents for complex tasks | Multi-Agent Teams |
| `research_workflow` | Two-agent research and writing workflow | Workflow Class |
| `pdf_rag_agent` | RAG with PDF documents and local embeddings | Knowledge Base |
| `hackernews_agent` | Custom function tool for HackerNews API | Custom Tools |

## Provider Recommendations

### Structured Output Examples

Examples using Pydantic models for structured output (`movie_script_generator`) work best with:

```bash
# Recommended - reliable structured output
python main.py --provider openai
python main.py --provider anthropic

# May work but less reliable
python main.py --provider openrouter
```

**Why?** OpenAI and Anthropic have native JSON mode support. OpenRouter proxies various models, some of which don't reliably return valid JSON.

### Tool-Using Examples

Examples using tools (`web_search_agent`, `finance_agent`, etc.) work with most providers:

```bash
python main.py                    # Default (OpenRouter)
python main.py --provider openai
python main.py --provider groq    # Fast, good for testing
```

### Local Embeddings

RAG examples (`pdf_rag_agent`) use SentenceTransformers for local embeddings - no API key needed for the vector operations:

```bash
# Uses local all-MiniLM-L6-v2 model for embeddings
python pdf_rag_agent/main.py --provider openai
```

## Running Examples

```bash
cd ~/ai_projects/development/agno-learning
source .venv/bin/activate

# Structured output (use OpenAI)
python 07_real_world/outskill_cohort3/movie_script_generator/main.py --provider openai --setting "Tokyo 2099"

# Web search
python 07_real_world/outskill_cohort3/web_search_agent/main.py --query "latest AI news"

# Finance data
python 07_real_world/outskill_cohort3/finance_agent/main.py --symbol NVDA

# Multi-agent team
python 07_real_world/outskill_cohort3/agent_team/main.py --query "NVDA stock analysis"

# Reasoning puzzle
python 07_real_world/outskill_cohort3/reasoning_agent/main.py --puzzle "missionaries"
```

## Dependencies

These examples require additional dependencies beyond the base `agno-learning` install:

```bash
# Already in pyproject.toml
pip install duckdb          # For CsvTools
pip install yfinance        # For YFinanceTools
pip install sentence-transformers  # For local embeddings

# May need for some examples
pip install crawl4ai        # For web scraping
pip install chromadb        # For vector storage alternative
```

## Original Source

These examples are adapted from the Outskill GenAI Engineering Cohort 3 curriculum, Week 12:
- Day 1: Agents, Tools, RAG, Workflows
- Day 2: MCP, Agent-to-Agent, App Builder

Adapted for the Agno framework with:
- Multi-provider support via `shared/model_config.py`
- Argparse CLI for all examples
- Consistent error handling
- README documentation for each example
