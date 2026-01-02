# Example 102: CSV Data Analyst

Analyze CSV files using natural language queries.

## Features

- Automatic CSV download and caching
- Natural language data queries
- Schema discovery and analysis
- Streaming output support

## Run the Example

```bash
# Basic usage with IMDB dataset
python main.py

# Custom query
python main.py --query "What is the average movie rating by genre?"

# Use your own CSV
python main.py --csv-url "https://example.com/data.csv" --query "Summarize the data"

# Stream output
python main.py --stream --query "List top 10 highest rated movies"
```

## Key Concepts

- **CsvTools**: Built-in tool for CSV file operations
- **Tool Calls**: Agent automatically uses tools to answer questions
- **Caching**: Downloaded files are cached locally
