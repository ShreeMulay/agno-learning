"""
Example #081: Data Quality Checker
Category: engineering/data
DESCRIPTION: Validates data quality rules across datasets - checks nulls, duplicates, ranges, formats
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"dataset": "customer_orders", "sample_size": 1000}

class QualityIssue(BaseModel):
    column: str = Field(description="Column with the issue")
    issue_type: str = Field(description="Type: null, duplicate, range, format, consistency")
    severity: str = Field(description="high, medium, low")
    count: int = Field(description="Number of affected rows")
    recommendation: str = Field(description="How to fix")

class DataQualityReport(BaseModel):
    dataset: str = Field(description="Dataset analyzed")
    total_rows: int = Field(description="Total rows checked")
    issues: list[QualityIssue] = Field(description="Quality issues found")
    quality_score: float = Field(description="Overall score 0-100")
    summary: str = Field(description="Executive summary")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Data Quality Checker",
        instructions=[
            "Analyze dataset metadata and sample data for quality issues",
            "Check for: null values, duplicates, out-of-range values, format violations",
            "Assess referential integrity and cross-column consistency",
            "Prioritize issues by business impact",
            "Provide actionable remediation steps"
        ],
        output_schema=DataQualityReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Data Quality Checker - Demo\n" + "=" * 60)
    query = f"""Analyze this dataset metadata for quality issues:
Dataset: {config['dataset']}
Sample size: {config['sample_size']} rows

Schema:
- order_id (INT, PK)
- customer_id (INT, FK)
- order_date (DATE)
- amount (DECIMAL)
- status (VARCHAR)
- email (VARCHAR)

Sample issues detected:
- 15 null customer_ids
- 3 duplicate order_ids
- 5 negative amounts
- 12 invalid email formats
- 8 future order_dates"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DataQualityReport):
        print(f"\nDataset: {result.dataset}")
        print(f"Rows checked: {result.total_rows:,}")
        print(f"Quality Score: {result.quality_score}/100")
        print(f"\nIssues Found ({len(result.issues)}):")
        for issue in result.issues:
            print(f"  [{issue.severity.upper()}] {issue.column}: {issue.issue_type} ({issue.count} rows)")
        print(f"\nSummary: {result.summary}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", "-d", default=DEFAULT_CONFIG["dataset"])
    parser.add_argument("--sample-size", "-s", type=int, default=DEFAULT_CONFIG["sample_size"])
    args = parser.parse_args()
    run_demo(get_agent(), {"dataset": args.dataset, "sample_size": args.sample_size})

if __name__ == "__main__": main()
