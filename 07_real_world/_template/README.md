# Example Name

Brief one-sentence description of what this agent does.

## Overview

One paragraph explaining the problem this agent solves, who would use it, and what makes it valuable.

## Use Cases

- **Use Case 1**: Description of a specific scenario
- **Use Case 2**: Description of another scenario
- **Use Case 3**: Description of a third scenario

## Patterns Used

| Pattern | Purpose |
|---------|---------|
| Tools | What external tools/APIs are used |
| Memory | How conversation state is managed |
| Knowledge | What documents/data sources are loaded |
| Structured Output | Output schema for typed responses |

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `param1` | str | `"default"` | What this parameter controls |
| `param2` | int | `10` | What this parameter controls |

## Running

### Basic Usage

```bash
cd 07_real_world/category/subcategory/XX_example_name
python main.py
```

### With Custom Configuration

```bash
python main.py --param1 "custom_value" --param2 20
```

### From Python

```python
from main import get_agent

# Default configuration
agent = get_agent()
response = agent.run("Your query here")

# Custom configuration
agent = get_agent(config={"param1": "custom", "param2": 20})
response = agent.run("Your query here")
```

## Example Output

```
Query: Example input query

Response:
Example output showing what the agent produces...
```

## Customization Guide

### Changing the Model

```python
from agno.models.openrouter import OpenRouter

agent = get_agent(model=OpenRouter(id="openai/gpt-4o"))
```

### Adding Custom Instructions

```python
# Modify the instructions list in get_agent()
instructions=[
    "Base instruction",
    "Your custom instruction here",
]
```

### Extending the Output Schema

```python
class CustomOutput(ExampleOutput):
    custom_field: str
    another_field: list[str]
```

## Dependencies

- `agno` - Agent framework
- Additional dependencies if any

## Related Examples

- [Related Example 1](../path/to/example) - Brief description
- [Related Example 2](../path/to/example) - Brief description

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests: `python -m pytest`
4. Submit a pull request
