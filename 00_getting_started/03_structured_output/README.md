# Lesson 03: Structured Output

Get type-safe, validated responses from your agents using Pydantic models.

## Concepts Covered

- **response_model**: Tell the agent what structure to return
- **Pydantic models**: Define your expected output shape
- **Validation**: Automatic type checking and validation
- **structured_outputs**: OpenAI's native structured output mode

## Why Structured Output?

Instead of parsing text responses, get Python objects directly:

```python
# Without structured output
response = agent.run("Analyze this movie")
# response.content = "The movie is good, 8/10, action genre..."
# Now you have to parse this text somehow...

# With structured output
class MovieReview(BaseModel):
    title: str
    rating: int  # 1-10
    genre: str
    summary: str

response = agent.run("Analyze this movie", response_model=MovieReview)
# response.content is a MovieReview object!
print(response.content.rating)  # 8
```

## How It Works

```python
from pydantic import BaseModel, Field
from agno.agent import Agent

class Recipe(BaseModel):
    """A cooking recipe."""
    name: str = Field(description="Name of the dish")
    ingredients: list[str] = Field(description="List of ingredients")
    steps: list[str] = Field(description="Cooking steps")
    prep_time_minutes: int = Field(description="Preparation time")

agent = Agent(
    model=model,
    response_model=Recipe,  # Agent will return Recipe objects
)

response = agent.run("Give me a recipe for chocolate chip cookies")
recipe = response.content  # This is a Recipe object!
print(recipe.name)
print(recipe.ingredients)
```

## Field Descriptions Matter

The `Field(description=...)` helps the LLM understand what to put in each field:

```python
class Person(BaseModel):
    name: str = Field(description="Full name of the person")
    age: int = Field(description="Age in years", ge=0, le=150)
    email: str = Field(description="Valid email address")
```

## Run the Example

```bash
# Analyze a movie
python main.py --movie "The Matrix"

# Get a recipe
python main.py --recipe "pasta carbonara"
```

## Exercises

1. Add a `director` field to the MovieReview model
2. Create your own model for a "BookSummary"
3. Try adding validation constraints (ge, le, min_length, etc.)

## Next Lesson

[04_streaming](../04_streaming/) - Stream responses in real-time for better UX.
