"""
Example #150: Customer Segmenter Agent
Category: industry/ecommerce
DESCRIPTION: Segments customers for targeted marketing and personalization
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"customer_count": 5000, "analysis_period": "12 months"}

class CustomerSegment(BaseModel):
    segment_name: str = Field(description="Segment name")
    size_percentage: float = Field(description="Percentage of customer base")
    characteristics: list[str] = Field(description="Key characteristics")
    avg_order_value: float = Field(description="Average order value")
    purchase_frequency: str = Field(description="Purchase frequency")
    recommended_tactics: list[str] = Field(description="Marketing tactics")

class SegmentationAnalysis(BaseModel):
    total_customers: int = Field(description="Total customers analyzed")
    segments: list[CustomerSegment] = Field(description="Customer segments")
    segmentation_method: str = Field(description="Segmentation methodology")
    key_insights: list[str] = Field(description="Key insights")
    high_value_focus: str = Field(description="High value customer strategy")
    at_risk_strategy: str = Field(description="At-risk customer strategy")
    growth_opportunities: list[str] = Field(description="Growth opportunities")
    data_quality_notes: str = Field(description="Data quality observations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Customer Segmenter",
        instructions=[
            "You are an expert e-commerce customer analytics specialist.",
            f"Segment customer base of approximately {cfg['customer_count']} customers",
            "Use RFM (Recency, Frequency, Monetary) analysis principles",
            "Identify actionable segments for marketing",
            "Balance segment granularity with actionability",
            "Provide specific tactics for each segment",
        ],
        output_schema=SegmentationAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Customer Segmenter Agent - Demo")
    print("=" * 60)
    query = f"""Segment our e-commerce customer base:
- Customer Count: {config['customer_count']}
- Analysis Period: {config['analysis_period']}
- Data Available: Purchase history, browse behavior, email engagement

Create actionable customer segments."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SegmentationAnalysis):
        print(f"\n📊 Analyzed: {result.total_customers:,} customers")
        print(f"📐 Method: {result.segmentation_method}")
        print(f"\n👥 Segments:")
        for seg in result.segments[:5]:
            print(f"\n  📌 {seg.segment_name} ({seg.size_percentage:.1f}%)")
            print(f"     AOV: ${seg.avg_order_value:.2f} | Frequency: {seg.purchase_frequency}")
            print(f"     Traits: {', '.join(seg.characteristics[:2])}")
            print(f"     Tactics: {seg.recommended_tactics[0]}")
        print(f"\n💎 High Value: {result.high_value_focus}")
        print(f"⚠️ At Risk: {result.at_risk_strategy}")

def main():
    parser = argparse.ArgumentParser(description="Customer Segmenter Agent")
    parser.add_argument("--customers", "-c", type=int, default=DEFAULT_CONFIG["customer_count"])
    parser.add_argument("--period", "-p", default=DEFAULT_CONFIG["analysis_period"])
    args = parser.parse_args()
    config = {"customer_count": args.customers, "analysis_period": args.period}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
