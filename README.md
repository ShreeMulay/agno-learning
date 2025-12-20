# Agno Learning Hub

A hands-on learning platform for building AI agents with [Agno](https://github.com/agno-agi/agno) (formerly phiData).

## What You'll Learn

| Module | Topics |
|--------|--------|
| **00 Getting Started** | Agents, providers, streaming, structured output |
| **01 Tools** | Built-in tools, custom tools, MCP integration |
| **02 Knowledge** | RAG with PDFs, URLs, vectors |
| **03 Memory** | Session state, user memories, history |
| **04 Teams** | Multi-agent collaboration patterns |
| **05 Workflows** | Orchestration, pipelines, human-in-loop |
| **06 Production** | AgentOS, FastAPI, databases, monitoring |
| **07 Real World** | 9 complete production applications |

## Quick Start

```bash
# Clone and enter directory
cd agno-learning

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Set up API keys
cp .env.example .env
# Edit .env with your API keys (at minimum, set OPENROUTER_API_KEY)

# Run your first agent
python 00_getting_started/01_hello_agent/main.py
```

## Supported LLM Providers

| Provider | Command |
|----------|---------|
| **OpenRouter** (default) | `python main.py` |
| OpenAI | `python main.py --provider openai` |
| Anthropic | `python main.py --provider anthropic` |
| Google | `python main.py --provider google` |
| Groq | `python main.py --provider groq` |
| Ollama (local) | `python main.py --provider ollama` |

## Project Structure

```
agno-learning/
├── shared/              # Shared utilities (model config, helpers)
├── 00_getting_started/  # Module 0: Basics
├── 01_tools/            # Module 1: Agent Tools
├── 02_knowledge/        # Module 2: RAG & Knowledge
├── 03_memory/           # Module 3: Persistent Memory
├── 04_teams/            # Module 4: Multi-Agent
├── 05_workflows/        # Module 5: Orchestration
├── 06_production/       # Module 6: Deployment
├── 07_real_world/       # Module 7: Complete Apps
└── sample_data/         # Test files for examples
```

## Requirements

- Python 3.12+
- At least one LLM API key (OpenRouter recommended)

## License

MIT
