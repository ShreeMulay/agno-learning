# Example 04: Code Review Agent

An agent that reviews code for issues, style, and improvements.

## Features

- Syntax and logic analysis
- Style recommendations
- Security issue detection
- Refactoring suggestions

## Architecture

```
Code Input → Code Analyzer → Issue Detection → Suggestions → Review Report
```

## Key Concepts

- **Structured Output**: Consistent review format
- **Instructions**: Coding standards and guidelines
- **Multi-pass**: Different review aspects

## Run the Example

```bash
# Review a file
python main.py --file path/to/code.py

# Review inline code
python main.py "def add(a, b): return a + b"
```

## Customization Ideas

1. Add language-specific rules
2. Integrate with GitHub PR reviews
3. Add auto-fix suggestions
4. Track metrics over time
