"""
Example #084: SQL Query Optimizer
Category: engineering/data
DESCRIPTION: Analyzes and optimizes SQL queries for better performance
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"database": "postgresql"}

class OptimizationSuggestion(BaseModel):
    issue: str = Field(description="Performance issue identified")
    impact: str = Field(description="high, medium, low")
    suggestion: str = Field(description="How to fix")
    expected_improvement: str = Field(description="Expected speedup")

class QueryOptimization(BaseModel):
    original_query: str = Field(description="Original SQL query")
    optimized_query: str = Field(description="Optimized version")
    suggestions: list[OptimizationSuggestion] = Field(description="Optimization suggestions")
    index_recommendations: list[str] = Field(description="Indexes to create")
    estimated_speedup: str = Field(description="Overall expected improvement")
    explanation: str = Field(description="Why these changes help")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="SQL Query Optimizer",
        instructions=[
            "Analyze SQL queries for performance issues",
            "Identify missing indexes, inefficient joins, full table scans",
            "Rewrite queries using optimal patterns",
            "Suggest index creation for common query patterns",
            "Explain optimizations in terms of query execution"
        ],
        output_schema=QueryOptimization, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  SQL Query Optimizer - Demo\n" + "=" * 60)
    query = f"""Optimize this {config['database']} query:

SELECT * FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN products p ON p.id = o.product_id
WHERE o.order_date > '2024-01-01'
  AND c.country = 'USA'
  AND p.category IN ('Electronics', 'Books')
ORDER BY o.order_date DESC

Table stats:
- orders: 10M rows, indexed on id only
- customers: 500K rows, indexed on id
- products: 50K rows, indexed on id"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, QueryOptimization):
        print(f"\nEstimated Speedup: {result.estimated_speedup}")
        print(f"\nSuggestions ({len(result.suggestions)}):")
        for s in result.suggestions:
            print(f"  [{s.impact.upper()}] {s.issue}")
            print(f"    Fix: {s.suggestion}")
        print(f"\nIndex Recommendations:")
        for idx in result.index_recommendations:
            print(f"  - {idx}")
        print(f"\nOptimized Query:\n{result.optimized_query[:400]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", "-d", default=DEFAULT_CONFIG["database"])
    args = parser.parse_args()
    run_demo(get_agent(), {"database": args.database})

if __name__ == "__main__": main()
