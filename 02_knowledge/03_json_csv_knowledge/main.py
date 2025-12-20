#!/usr/bin/env python3
"""
Lesson 03: JSON and CSV Knowledge

Concepts covered:
- Loading JSON data into knowledge base
- Loading CSV data into knowledge base
- Querying structured data naturally
- Combining multiple data sources

Run: python main.py
     python main.py --json ./data.json
     python main.py --csv ./data.csv
     python main.py --query "What products do you have?"
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_sample_json(output_path: Path) -> None:
    """Create sample JSON data for demonstration."""
    products = [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "category": "Electronics",
            "price": 89.99,
            "rating": 4.5,
            "description": "High-quality wireless headphones with noise cancellation",
            "in_stock": True,
        },
        {
            "id": 2,
            "name": "Mechanical Keyboard",
            "category": "Electronics",
            "price": 149.99,
            "rating": 4.8,
            "description": "RGB mechanical keyboard with Cherry MX switches",
            "in_stock": True,
        },
        {
            "id": 3,
            "name": "Running Shoes",
            "category": "Sports",
            "price": 129.99,
            "rating": 4.3,
            "description": "Lightweight running shoes with excellent cushioning",
            "in_stock": True,
        },
        {
            "id": 4,
            "name": "Yoga Mat",
            "category": "Sports",
            "price": 39.99,
            "rating": 4.6,
            "description": "Non-slip yoga mat, 6mm thick, eco-friendly material",
            "in_stock": False,
        },
        {
            "id": 5,
            "name": "Coffee Maker",
            "category": "Home",
            "price": 79.99,
            "rating": 4.4,
            "description": "12-cup programmable coffee maker with thermal carafe",
            "in_stock": True,
        },
        {
            "id": 6,
            "name": "Standing Desk",
            "category": "Furniture",
            "price": 399.99,
            "rating": 4.7,
            "description": "Electric height-adjustable standing desk, 60 inch wide",
            "in_stock": True,
        },
    ]
    
    with open(output_path, "w") as f:
        json.dump(products, f, indent=2)
    
    print(f"Created sample JSON: {output_path}")


def create_sample_csv(output_path: Path) -> None:
    """Create sample CSV data for demonstration."""
    csv_content = """id,name,email,department,join_date,salary
1,Alice Johnson,alice@company.com,Engineering,2021-03-15,95000
2,Bob Smith,bob@company.com,Marketing,2020-07-01,75000
3,Carol Davis,carol@company.com,Engineering,2022-01-10,88000
4,David Wilson,david@company.com,Sales,2019-11-20,82000
5,Eva Martinez,eva@company.com,HR,2023-02-28,65000
6,Frank Brown,frank@company.com,Engineering,2021-09-05,92000
"""
    output_path.write_text(csv_content)
    print(f"Created sample CSV: {output_path}")



def create_data_agent(model, knowledge):
    """Create a data assistant agent."""
    return Agent(
        model=model,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "You are a data assistant with access to product information.",
            "Answer questions based on the data available.",
            "Provide specific details like prices, ratings, and availability.",
            "Format responses clearly with relevant data.",
        ],
        markdown=True,
    )


def main():
    """Demonstrate JSON and CSV knowledge bases."""
    parser = argparse.ArgumentParser(
        description="JSON and CSV Knowledge demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--json",
        type=str,
        help="Path to JSON file",
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Path to CSV file",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What products are available in Electronics category? List them with prices.",
        help="Question to ask about the data",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild the knowledge base",
    )
    args = parser.parse_args()

    print_header("Lesson 03: JSON and CSV Knowledge")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    # Set up paths
    project_root = Path(__file__).parent.parent.parent
    sample_dir = project_root / "sample_data"
    sample_dir.mkdir(exist_ok=True)
    lancedb_path = project_root / ".lancedb"

    # Create or use sample data
    json_path = Path(args.json) if args.json else sample_dir / "products.json"
    csv_path = Path(args.csv) if args.csv else sample_dir / "employees.csv"

    if not args.json and (not json_path.exists() or args.rebuild):
        print_section("Creating Sample Data")
        create_sample_json(json_path)
        create_sample_csv(csv_path)

    print_section("Building Knowledge Base")
    print(f"JSON: {json_path}")
    print(f"Vector DB: {lancedb_path}")

    try:
        # Create knowledge base with JSON content
        knowledge = Knowledge(
            name="json_knowledge",
            vector_db=LanceDb(
                table_name="json_knowledge",
                uri=str(lancedb_path),
            ),
        )
        
        print("Indexing JSON data...")
        knowledge.add_content(path=str(json_path))
        print("Knowledge base ready!")
        
    except Exception as e:
        print(f"Error building knowledge base: {e}")
        print("\nTip: Make sure you have the required dependencies:")
        print("  pip install lancedb")
        sys.exit(1)

    print_section("Creating Data Assistant")
    
    agent = create_data_agent(model, knowledge)

    print_section("Query")
    print(f"Question: {args.query}\n")
    
    print("Answer:")
    print("-" * 60)
    agent.print_response(args.query)
    print("-" * 60)

    print_section("Try More Queries")
    example_queries = [
        "What is the most expensive product?",
        "Which products have a rating above 4.5?",
        "What products are currently out of stock?",
        "List all products under $100",
    ]
    
    for q in example_queries:
        print(f"  - {q}")
    
    print("\nRun: python main.py --query \"Your question\"")


if __name__ == "__main__":
    main()
