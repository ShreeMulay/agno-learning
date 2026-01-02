# Example 104: Code to Diagram Generator

Generate UML diagrams from Python source code.

## Features

- Multiple diagram types (class, sequence, flowchart)
- PlantUML and Mermaid output formats
- Automatic code analysis
- Built-in example for quick testing

## Run the Example

```bash
# Basic usage (uses built-in example)
python main.py

# Analyze your own file
python main.py --file-path /path/to/your/code.py

# Generate sequence diagram
python main.py --diagram-type sequence

# Output as PlantUML
python main.py --output-format plantuml

# Stream output
python main.py --stream
```

## Diagram Types

| Type | Description |
|------|-------------|
| `class` | Classes, attributes, methods, relationships |
| `sequence` | Function calls and execution flow |
| `flowchart` | Program flow with decision points |

## Output Formats

- **Mermaid**: Renders in GitHub, GitLab, and many documentation tools
- **PlantUML**: Industry standard, requires PlantUML server to render

## Key Concepts

- **FileTools**: Read source code files
- **Code Analysis**: AI understands code structure
- **UML Generation**: Proper diagram notation
