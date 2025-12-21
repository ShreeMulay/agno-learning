"""
Example #085: Data Catalog Curator
Category: engineering/data
DESCRIPTION: Manages data catalog metadata - descriptions, lineage, ownership, tags
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"asset_type": "table"}

class ColumnMetadata(BaseModel):
    name: str = Field(description="Column name")
    description: str = Field(description="Business description")
    data_type: str = Field(description="Data type")
    pii: bool = Field(description="Contains PII")
    tags: list[str] = Field(description="Classification tags")

class CatalogEntry(BaseModel):
    asset_name: str = Field(description="Table/view/dataset name")
    asset_type: str = Field(description="table, view, dashboard, etc.")
    description: str = Field(description="Business description")
    owner: str = Field(description="Data owner team/person")
    domain: str = Field(description="Business domain")
    columns: list[ColumnMetadata] = Field(description="Column metadata")
    tags: list[str] = Field(description="Asset-level tags")
    quality_score: float = Field(description="Data quality score")
    usage_frequency: str = Field(description="high, medium, low")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Data Catalog Curator",
        instructions=[
            "Generate comprehensive metadata for data assets",
            "Write clear business descriptions for technical columns",
            "Identify PII and sensitive data fields",
            "Suggest appropriate tags and classifications",
            "Recommend data ownership based on domain"
        ],
        output_schema=CatalogEntry, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Data Catalog Curator - Demo\n" + "=" * 60)
    query = f"""Create catalog entry for this {config['asset_type']}:

Name: customer_transactions
Columns:
- txn_id (BIGINT)
- customer_id (INT)
- email (VARCHAR)
- ssn_last4 (CHAR(4))
- amount (DECIMAL)
- txn_date (TIMESTAMP)
- merchant_category (VARCHAR)
- ip_address (VARCHAR)

Context: Used by finance team for fraud detection and reporting"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CatalogEntry):
        print(f"\nAsset: {result.asset_name} ({result.asset_type})")
        print(f"Owner: {result.owner}")
        print(f"Domain: {result.domain}")
        print(f"Quality Score: {result.quality_score}")
        print(f"Tags: {', '.join(result.tags)}")
        print(f"\nColumns ({len(result.columns)}):")
        for col in result.columns:
            pii_flag = " [PII]" if col.pii else ""
            print(f"  - {col.name}{pii_flag}: {col.description[:50]}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset-type", "-t", default=DEFAULT_CONFIG["asset_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"asset_type": args.asset_type})

if __name__ == "__main__": main()
