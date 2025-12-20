# MEGA Examples - Development Conventions

## Overview

This subproject builds 235 real-world agent examples. Follow these conventions for consistency.

## File Structure

### Example Directory
```
XX_example_name/
├── main.py     # Agent implementation (required)
└── README.md   # Documentation (required)
```

### main.py Template
```python
"""
Example #XXX: Example Name
Category: category/subcategory

DESCRIPTION:
One paragraph explaining what this agent does and when to use it.

PATTERNS:
- Pattern 1 (e.g., Tools + Structured Output)
- Pattern 2 (e.g., Memory)

ARGUMENTS:
- arg1 (str): Description. Default: "value"
- arg2 (int): Description. Default: 10
"""

from agno.agent import Agent
# ... other imports

DEFAULT_CONFIG = {
    "arg1": "default_value",
    "arg2": 10,
}

def get_agent(model=None, config=None):
    """
    Create the agent with optional configuration.
    
    Args:
        model: Override default model (for testing/portal)
        config: Dict of configuration options
    
    Returns:
        Configured Agent instance
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        # ... configuration
    )

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Example Name")
    parser.add_argument("--arg1", default=DEFAULT_CONFIG["arg1"])
    parser.add_argument("--arg2", type=int, default=DEFAULT_CONFIG["arg2"])
    args = parser.parse_args()
    
    agent = get_agent(config=vars(args))
    # ... run agent

if __name__ == "__main__":
    main()
```

## Naming Conventions

### Directories
- Use `snake_case` for all directories
- Prefix with 2-digit number: `01_lead_qualifier`
- Keep names concise but descriptive

### Files
- Main module: `main.py`
- Docs: `README.md`
- Data: `data/` subdirectory if needed
- Tests: `test_main.py` if custom tests needed

### Code
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Pydantic models: `PascalCase` with descriptive names

## Required Components

### 1. Docstring Header
Every `main.py` must start with:
```python
"""
Example #XXX: Example Name
Category: category/subcategory

DESCRIPTION:
...

PATTERNS:
...

ARGUMENTS:
...
"""
```

### 2. DEFAULT_CONFIG
Export configurable parameters:
```python
DEFAULT_CONFIG = {
    "param_name": "default_value",
}
```

### 3. get_agent() Function
```python
def get_agent(model=None, config=None) -> Agent:
    # Must work with no arguments
    # Must accept model override
    # Must accept config dict
```

### 4. CLI Interface
```python
def main():
    parser = argparse.ArgumentParser()
    # Add args matching DEFAULT_CONFIG
    args = parser.parse_args()
    agent = get_agent(config=vars(args))
    # Run demo
```

### 5. Demo Mode
Agent must work without external APIs using:
- Sample/mock data
- Graceful fallbacks
- Default parameters

## Testing Requirements

### Standard Tests (Required)
Every example must pass before commit:

```python
# test_main.py (or in shared/testing/smoke_test.py)
def test_import():
    from main import get_agent, DEFAULT_CONFIG
    
def test_agent_creation():
    agent = get_agent()
    assert agent is not None
    
def test_smoke():
    agent = get_agent()
    response = agent.run("Test query")
    assert response is not None
```

### Running Tests
```bash
# Single example
cd examples/07_real_world/business/sales/01_lead_qualifier
python -m pytest

# All examples
python shared/testing/smoke_test.py

# Category
python shared/testing/smoke_test.py --category business
```

## Model Configuration

### Default Model
```python
from agno.models.openrouter import OpenRouter

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")
```

### Model Override
Always accept model parameter:
```python
def get_agent(model=None, config=None):
    return Agent(
        model=model or default_model(),
        ...
    )
```

## Error Handling

### Structured Output Fallback
When using `response_model`, handle parsing failures:
```python
response = agent.run(query)

if response.parsed:
    result = response.parsed
else:
    # Fallback: extract from raw content
    print(f"Raw response: {response.content}")
```

### External API Fallback
```python
try:
    data = external_api.fetch()
except Exception as e:
    print(f"API unavailable, using cached data: {e}")
    data = load_cached_data()
```

## Git Workflow

### Commits
One commit per example:
```bash
git add examples/07_real_world/business/sales/01_lead_qualifier/
git commit -m "feat(examples): add lead qualifier agent (#001)"
```

### Commit Message Format
```
feat(examples): add <example_name> (#XXX)
```

Where XXX is the global example number.

## Documentation

### README.md Template
```markdown
# Example Name

Brief description of what this agent does.

## Use Cases

- Use case 1
- Use case 2

## Patterns Used

- **Tools**: What external tools are used
- **Memory**: How state is managed
- **Knowledge**: What documents/data are loaded

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| param1 | str | "value" | What it controls |

## Running

\`\`\`bash
python main.py
python main.py --param1 "custom"
\`\`\`

## Example Output

\`\`\`
Expected output...
\`\`\`

## Customization

How to adapt this example for different use cases.
```

## External Integrations

### API Keys
Store in `.env`, never commit:
```python
import os
api_key = os.getenv("SERVICE_API_KEY")
```

### Rate Limiting
Respect API limits:
```python
import time
for item in items:
    process(item)
    time.sleep(0.1)  # Rate limit
```

### Caching
Cache expensive API calls:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_data(query: str):
    return api.search(query)
```

## Beads Integration

### Creating Issues
```bash
bd create "Implement 01_lead_qualifier" \
  --description="Lead scoring agent using Knowledge + Structured Output" \
  -t task -p 2 \
  --deps discovered-from:mega-examples-epic
```

### Updating Progress
```bash
bd update <id> --status in_progress
# ... implement ...
bd close <id> --reason "Completed: passes all smoke tests"
```

## Quality Checklist

Before committing any example:

- [ ] Docstring complete with example number
- [ ] DEFAULT_CONFIG exported
- [ ] get_agent() works with no arguments
- [ ] CLI exposes all config options
- [ ] Demo mode works without external APIs
- [ ] README.md documents usage
- [ ] Smoke test passes
- [ ] Code follows style conventions
