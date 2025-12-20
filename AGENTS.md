# Agno Learning Hub

A hands-on learning platform for Agno (formerly phiData) that teaches you to build AI agents through runnable examples.

**See**: `openspec/AGENTS.md` for detailed specifications.

## Quick Start

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Set up API keys
cp .env.example .env
# Edit .env with your API keys

# Run your first agent
python 00_getting_started/01_hello_agent/main.py
```

## Project Structure

```
agno-learning/
├── shared/                      # Shared utilities
│   ├── model_config.py          # Multi-provider LLM config
│   └── utils.py                 # Common helpers
├── 00_getting_started/          # Module 0: Basics
├── 01_tools/                    # Module 1: Agent Tools
├── 02_knowledge/                # Module 2: RAG & Knowledge
├── 03_memory/                   # Module 3: Persistent Memory
├── 04_teams/                    # Module 4: Multi-Agent
├── 05_workflows/                # Module 5: Orchestration
├── 06_production/               # Module 6: Deployment
├── 07_real_world/               # Module 7: Complete Apps
└── sample_data/                 # Test files for examples
```

## Tech Stack

- **Framework**: Agno v2.3.x
- **Python**: 3.12+
- **Vector DB**: LanceDB (local, no Docker)
- **Package Manager**: uv (preferred) or pip

## LLM Providers

All examples support multiple providers via `shared/model_config.py`:

| Provider | Env Variable | Default Model |
|----------|--------------|---------------|
| **OpenRouter** | `OPENROUTER_API_KEY` | `anthropic/claude-3.5-sonnet` |
| **OpenAI** | `OPENAI_API_KEY` | `gpt-4o` |
| **Anthropic** | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5` |
| **Google** | `GOOGLE_AI_API_KEY` | `gemini-2.0-flash` |
| **Groq** | `GROQ_API_KEY` | `llama-3.3-70b-versatile` |
| **Ollama** | `OLLAMA_HOST` | `llama3.2` |

## Running Examples

Each lesson has a `main.py` with argparse support:

```bash
# Default provider (OpenRouter)
python 00_getting_started/01_hello_agent/main.py

# Specific provider
python 00_getting_started/01_hello_agent/main.py --provider openai

# Custom model
python 00_getting_started/01_hello_agent/main.py --provider openrouter --model deepseek/deepseek-chat-v3

# List available providers
python -m shared.model_config
```

## Development Guidelines

### Example Structure

Each lesson folder contains:
- `README.md` - Explanation, concepts, exercises
- `main.py` - Complete runnable example (50-100 lines)

### Code Style

- Python: PEP 8, type hints required
- Error handling: Try/except with meaningful messages
- Logging: Use `print()` for learning output
- Docstrings: Google style for functions

### API Keys

Store in `.env` file (gitignored) or `~/.bash_secrets`:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Beads Issue Tracking

This project uses **bd** (beads) for issue tracking.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

---

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work**
2. **Run quality gates** (if code changed): `ruff check .`
3. **Update issue status**
4. **PUSH TO REMOTE**:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Verify** - All changes committed AND pushed

**CRITICAL**: Work is NOT complete until `git push` succeeds.
