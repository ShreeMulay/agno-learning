#!/usr/bin/env python3
"""Example 06: Data Analysis Agent - Analyze data and generate insights.

An agent that analyzes datasets and provides actionable insights.

Run with:
    python main.py --data sales.csv "What are the key trends?"
    python main.py  # Uses demo data
"""

import argparse
import json
import sys
from pathlib import Path
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class DataInsight(BaseModel):
    """A single data insight."""
    title: str = Field(description="Insight title")
    finding: str = Field(description="What the data shows")
    significance: str = Field(description="Why this matters")
    recommendation: str = Field(description="Suggested action")


class DataAnalysis(BaseModel):
    """Complete data analysis result."""
    summary: str = Field(description="Executive summary")
    key_metrics: dict[str, str] = Field(description="Important metrics")
    insights: list[DataInsight] = Field(description="Key insights")
    trends: list[str] = Field(description="Identified trends")
    recommendations: list[str] = Field(description="Action items")
    visualization_suggestions: list[str] = Field(description="Charts to create")


# Sample data for demo
DEMO_DATA = {
    "sales_data": [
        {"month": "Jan", "revenue": 45000, "units": 150, "returns": 5},
        {"month": "Feb", "revenue": 52000, "units": 175, "returns": 8},
        {"month": "Mar", "revenue": 48000, "units": 160, "returns": 3},
        {"month": "Apr", "revenue": 61000, "units": 210, "returns": 7},
        {"month": "May", "revenue": 58000, "units": 195, "returns": 4},
        {"month": "Jun", "revenue": 72000, "units": 240, "returns": 6},
    ],
    "metadata": {
        "period": "Q1-Q2 2024",
        "product": "Widget Pro",
        "region": "North America",
    }
}


def create_data_agent(model):
    """Create a data analysis agent."""
    
    return Agent(
        name="DataAnalyst",
        model=model,
        instructions=[
            "You are a data analyst expert.",
            "Analyze data to find meaningful patterns and insights.",
            "Focus on actionable recommendations.",
            "Identify trends, anomalies, and opportunities.",
            "Suggest appropriate visualizations.",
            "Be specific with numbers and percentages.",
        ],
        markdown=True,
    )


def load_data(file_path: str) -> dict:
    """Load data from file."""
    path = Path(file_path)
    if path.suffix == '.json':
        return json.loads(path.read_text())
    elif path.suffix == '.csv':
        import csv
        with open(path) as f:
            reader = csv.DictReader(f)
            return {"data": list(reader)}
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_data_agent(model)


def main():
    parser = argparse.ArgumentParser(description="Data Analysis Agent")
    add_model_args(parser)
    parser.add_argument(
        "--data", "-d", type=str, default=None,
        help="Path to data file (JSON or CSV)"
    )
    parser.add_argument(
        "question", type=str, nargs="?",
        default="Analyze this data and provide key insights",
        help="Analysis question"
    )
    args = parser.parse_args()

    print_header("Data Analysis Agent")
    
    # Load data
    if args.data:
        try:
            data = load_data(args.data)
            source = args.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return
    else:
        data = DEMO_DATA
        source = "demo (sales data)"
    
    print_section("Data Source")
    print(f"  Source: {source}")
    print(f"  Records: {len(data.get('sales_data', data.get('data', [])))}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_data_agent(model)
    
    prompt = f"""
Analyze this data and answer: {args.question}

Data:
{json.dumps(data, indent=2)}
"""
    
    print_section("Analyzing...")
    response = agent.run(prompt, output_schema=DataAnalysis)
    analysis = response.content
    
    print_section("Summary")
    print(f"  {analysis.summary}")
    
    print_section("Key Metrics")
    for metric, value in analysis.key_metrics.items():
        print(f"  • {metric}: {value}")
    
    print_section("Insights")
    for i, insight in enumerate(analysis.insights, 1):
        print(f"\n  {i}. {insight.title}")
        print(f"     Finding: {insight.finding}")
        print(f"     Significance: {insight.significance}")
        print(f"     Action: {insight.recommendation}")
    
    print_section("Trends")
    for trend in analysis.trends:
        print(f"  📈 {trend}")
    
    print_section("Recommendations")
    for rec in analysis.recommendations:
        print(f"  → {rec}")
    
    print_section("Suggested Visualizations")
    for viz in analysis.visualization_suggestions:
        print(f"  📊 {viz}")


if __name__ == "__main__":
    main()
