# Lesson 03: JSON and CSV Knowledge

Load structured data files into your agent's knowledge base.

## Concepts Covered

- **JSONKnowledge**: Load JSON data
- **CSVKnowledge**: Load CSV/spreadsheet data  
- **Structured data**: Working with tabular information
- **Data transformation**: Converting data to searchable text

## Why Structured Data?

Structured data (JSON, CSV) contains:
- Product catalogs
- Customer records
- Configuration data
- API responses
- Database exports

Agents can answer questions about this data naturally.

## How It Works

```python
from agno.knowledge.json_file import JSONKnowledge
from agno.knowledge.csv_file import CSVKnowledge
from agno.vectordb.lancedb import LanceDb

# JSON knowledge
json_knowledge = JSONKnowledge(
    path="./data/products.json",
    vector_db=LanceDb(table_name="json_data", uri="./lancedb"),
)

# CSV knowledge
csv_knowledge = CSVKnowledge(
    path="./data/customers.csv",
    vector_db=LanceDb(table_name="csv_data", uri="./lancedb"),
)

# Load data
json_knowledge.load()
csv_knowledge.load()
```

## Run the Example

```bash
# Use sample data
python main.py

# Custom JSON file
python main.py --json ./my_data.json

# Custom CSV file
python main.py --csv ./my_data.csv

# Query the data
python main.py --query "Which product has the highest price?"
```

## Data Format Tips

### JSON
```json
[
  {"id": 1, "name": "Product A", "price": 99.99},
  {"id": 2, "name": "Product B", "price": 149.99}
]
```

### CSV
```csv
id,name,price,category
1,Product A,99.99,Electronics
2,Product B,149.99,Electronics
```

## Exercises

1. Load a product catalog and create a shopping assistant
2. Import customer data and build a CRM helper
3. Combine JSON and CSV data in one agent

## Next Lesson

[04_vector_search](../04_vector_search/) - Understand vector search in depth.
