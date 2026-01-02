# Example 103: EDA Visualization Agent

Perform exploratory data analysis and create visualizations using AI-generated Python code.

## Features

- Multiple analysis types (overview, distribution, correlation)
- Automatic code generation and execution
- Creates and saves matplotlib/seaborn visualizations
- Streaming output support

## Run the Example

```bash
# Basic overview analysis
python main.py

# Distribution analysis
python main.py --analysis-type distribution

# Correlation analysis with custom output
python main.py --analysis-type correlation --output-dir ./charts

# Use your own dataset
python main.py --dataset-url "https://example.com/data.csv"
```

## Analysis Types

| Type | Description |
|------|-------------|
| `overview` | Data shape, types, missing values, correlation heatmap |
| `distribution` | Histograms, box plots, outlier detection |
| `correlation` | Correlation matrix, top correlations, scatter plots |

## Key Concepts

- **PythonTools**: Execute generated Python code
- **Code Generation**: AI writes analysis scripts
- **Automatic pip install**: Dependencies installed as needed
