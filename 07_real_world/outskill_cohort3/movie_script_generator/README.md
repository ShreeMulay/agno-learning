# Example 101: Movie Script Generator

Generate creative movie scripts using structured output with Pydantic models.

## Features

- Structured JSON output with Pydantic validation
- Configurable setting, genre, and character count
- Creative AI-generated storylines and endings

## Run the Example

```bash
# Basic usage
python main.py

# Custom setting
python main.py --setting "Mars colony in 2150"

# Specify genre and characters
python main.py --setting "Victorian London" --genre "mystery" --num-characters 4

# Use different provider
python main.py --provider anthropic --setting "Tokyo 2077"
```

## Output Schema

```python
class MovieScript(BaseModel):
    name: str          # Movie title
    setting: str       # Detailed setting
    genre: str         # Genre classification
    characters: list   # Main character names
    storyline: str     # 3-5 sentence plot
    ending: str        # How it ends
```

## Key Concepts

- **Structured Output**: Using `response_model` for typed responses
- **Pydantic Integration**: Schema validation and serialization
- **Creative Prompting**: Guiding AI for consistent creative output
