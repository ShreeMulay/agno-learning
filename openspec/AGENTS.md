# Agno Learning Hub - OpenSpec

## Project Overview

A comprehensive, hands-on learning platform for Agno (formerly phiData) that teaches developers to build AI agents through 33 runnable examples organized into 8 progressive modules.

## Goals

1. **Learn by doing** - Every concept has a runnable example
2. **Production-ready patterns** - Complete examples with error handling
3. **Multi-provider support** - Easily switch between LLM providers
4. **Progressive complexity** - From "Hello Agent" to multi-agent systems

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | Agno v2.3.x | Target learning framework |
| **Python** | 3.12+ | Agno requirement |
| **Package Manager** | uv | Fast, pyproject.toml native |
| **Vector DB** | LanceDB | Local, no Docker required |
| **LLM Default** | OpenRouter | Multi-model access |

## Module Curriculum

### Module 0: Getting Started (Foundation)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_hello_agent | `main.py` | Agent, Model, run(), print_response() |
| 02_multi_provider | `main.py` | Provider switching, model config |
| 03_structured_output | `main.py` | Pydantic, response_model, validation |
| 04_streaming | `main.py` | Streaming responses, async |

### Module 1: Tools (Extending Capabilities)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_builtin_tools | `main.py` | DuckDuckGo, Calculator, FileTools |
| 02_custom_tools | `main.py` | Function decorators, docstrings |
| 03_tool_context | `main.py` | RunContext, session_state |
| 04_mcp_tools | `main.py` | MCPTools, external servers |

### Module 2: Knowledge (RAG)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_pdf_knowledge | `main.py` | PDFKnowledge, chunking |
| 02_url_knowledge | `main.py` | URLKnowledge, web scraping |
| 03_json_csv_knowledge | `main.py` | JSONKnowledge, CSVKnowledge |
| 04_vector_search | `main.py` | LanceDB, embeddings, search |

### Module 3: Memory (Persistence)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_session_state | `main.py` | session_state dict |
| 02_user_memories | `main.py` | enable_user_memories, SqliteDb |
| 03_agentic_memory | `main.py` | enable_agentic_memory |
| 04_history | `main.py` | add_history_to_context |

### Module 4: Teams (Multi-Agent)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_basic_team | `main.py` | Team, agents list |
| 02_coordinate_mode | `main.py` | Leader coordination |
| 03_route_mode | `main.py` | respond_directly |
| 04_collaborate_mode | `main.py` | delegate_to_all_members |

### Module 5: Workflows (Orchestration)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_basic_workflow | `main.py` | Workflow, @step decorator |
| 02_conditional_flow | `main.py` | Branching logic |
| 03_parallel_steps | `main.py` | Concurrent execution |
| 04_human_in_loop | `main.py` | Approval gates |

### Module 6: Production (Deployment)

| Lesson | File | Concepts |
|--------|------|----------|
| 01_agent_os | `main.py` | AgentOS, get_app() |
| 02_fastapi_integration | `main.py` | Custom routes, middleware |
| 03_database_config | `main.py` | PostgresDb, migrations |
| 04_monitoring | `main.py` | Metrics, logging |

### Module 7: Real World (Complete Apps)

| Example | Description | Key Patterns |
|---------|-------------|--------------|
| 01_research_assistant | Web search + summarize | Tools + Knowledge |
| 02_doc_qa_system | PDF Q&A with RAG | Knowledge + Memory |
| 03_customer_support | Multi-agent routing | Teams + Memory |
| 04_code_review_agent | GitHub PR review | Tools + Structured Output |
| 05_blog_post_generator | Research-to-blog pipeline | Workflows + Teams |
| 06_data_analysis_agent | CSV/Excel analysis | Tools + Structured Output |
| 07_personal_knowledge_base | Persistent notes system | Knowledge + Memory |
| 08_clinical_decision_support | Medical domain RAG | Knowledge + Structured Output |
| 09_build_your_own_template | Blank scaffold | All patterns |

## Example Structure

Each lesson follows this structure:

```
XX_module/YY_lesson/
├── README.md     # Concepts, explanation, exercises
└── main.py       # Complete runnable example (50-100 lines)
```

### main.py Template

```python
#!/usr/bin/env python3
"""
Lesson Title - Brief description

Concepts covered:
- Concept 1
- Concept 2

Run: python main.py [--provider openai] [--model gpt-4o]
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_response


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description=__doc__)
    add_model_args(parser)
    # Add lesson-specific args here
    args = parser.parse_args()
    
    # Get model
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    print_header("Lesson Title")
    
    # Lesson implementation here
    agent = Agent(
        model=model,
        instructions="You are a helpful assistant.",
    )
    
    response = agent.run("Hello, world!")
    print_response(response)


if __name__ == "__main__":
    main()
```

## Development Workflow

1. **Start session**: `bd ready` to find available work
2. **Claim issue**: `bd update <id> --status in_progress`
3. **Implement lesson**: Follow the template above
4. **Test locally**: `python XX_module/YY_lesson/main.py`
5. **Complete work**: `bd close <id>`
6. **Push changes**: `bd sync && git push`

## Quality Standards

- [ ] All examples run without errors
- [ ] Error messages are helpful
- [ ] Each example demonstrates exactly one concept
- [ ] README explains the "why" not just the "how"
- [ ] Code follows PEP 8 with type hints
