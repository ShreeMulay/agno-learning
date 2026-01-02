#!/usr/bin/env python3
"""Example #102: CSV Data Analyst
Category: outskill_cohort3/data_analysis

DESCRIPTION:
Analyzes CSV files using natural language queries. The agent can read CSV files,
understand their structure, and answer questions about the data using SQL-like
operations under the hood.

PATTERNS:
- Tools (CsvTools for file operations)
- Data Analysis (query and summarize data)

ARGUMENTS:
- csv_url (str): URL to a CSV file. Default: IMDB movie dataset
- query (str): Natural language question about the data. Default: "Which year had the most movies?"
"""

import argparse
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "csv_url": "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
    "query": "In which year were the highest number of movies released?",
}

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.csv_toolkit import CsvTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_agent(model, csv_path: str):
    """Create the CSV data analyst agent."""
    return Agent(
        name="CsvDataAnalyst",
        model=model,
        tools=[CsvTools(csvs=[csv_path])],
        instructions=[
            "You are a data analyst expert.",
            "First, get the list of available CSV files.",
            "Then, check the columns in the file to understand the schema.",
            "Finally, run queries to answer the user's question.",
            "Always explain your findings clearly.",
        ],
        show_tool_calls=True,
        markdown=True,
    )


def get_agent(model=None):
    """Get agent instance for GUI integration."""
    if model is None:
        model = get_model()
    return create_agent(model, DEFAULT_CONFIG["csv_url"])


def download_csv(url: str, local_path: Path) -> Path:
    """Download CSV from URL if not already cached."""
    if local_path.exists():
        return local_path
    
    try:
        import httpx
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(response.content)
        return local_path
    except Exception as e:
        raise RuntimeError(f"Failed to download CSV: {e}") from e


def main():
    parser = argparse.ArgumentParser(
        description="Analyze CSV files with natural language queries"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--csv-url",
        type=str,
        default=DEFAULT_CONFIG["csv_url"],
        help="URL to CSV file (will be downloaded and cached)"
    )
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_CONFIG["query"],
        help="Natural language question about the data"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming output"
    )
    
    args = parser.parse_args()
    
    print_header("CSV Data Analyst")
    
    cache_dir = Path(__file__).parent / "cache"
    csv_filename = args.csv_url.split("/")[-1]
    local_csv = cache_dir / csv_filename
    
    print_section("Loading Data")
    try:
        csv_path = download_csv(args.csv_url, local_csv)
        print(f"  CSV: {csv_path.name}")
    except Exception as e:
        print(f"  Error: {e}")
        sys.exit(1)
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model, str(csv_path))
    
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    print_section("Analysis")
    
    try:
        if args.stream:
            response = agent.run(args.query, stream=True)
            for chunk in response:
                if hasattr(chunk, 'content') and chunk.content:
                    print(chunk.content, end="", flush=True)
            print()
        else:
            response = agent.run(args.query)
            print(response.content)
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
