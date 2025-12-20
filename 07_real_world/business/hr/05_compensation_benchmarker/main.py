"""
Example #045: Compensation Benchmarker
Category: business/hr

DESCRIPTION:
Analyzes market compensation data to recommend salary ranges
for roles based on location, experience, and industry.

PATTERNS:
- Knowledge (comp data patterns)
- Structured Output (CompAnalysis)
- Reasoning (market positioning)

ARGUMENTS:
- role (str): Job title
- location (str): Geographic location
- experience_years (int): Years of experience
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "role": "Senior Software Engineer",
    "location": "San Francisco Bay Area",
    "experience_years": 7,
    "company_size": "Series B startup (100-200 employees)",
    "industry": "FinTech",
}


class SalaryRange(BaseModel):
    percentile_25: int = Field(description="25th percentile salary")
    percentile_50: int = Field(description="Median salary")
    percentile_75: int = Field(description="75th percentile salary")
    percentile_90: int = Field(description="90th percentile salary")


class CompAnalysis(BaseModel):
    role: str = Field(description="Job title analyzed")
    location: str = Field(description="Location")
    experience_level: str = Field(description="junior/mid/senior/staff/principal")
    base_salary_range: SalaryRange = Field(description="Base salary ranges")
    recommended_range_min: int = Field(description="Recommended min offer")
    recommended_range_max: int = Field(description="Recommended max offer")
    equity_range: str = Field(description="Typical equity range")
    bonus_typical: str = Field(description="Typical bonus structure")
    total_comp_estimate: str = Field(description="Total compensation range")
    market_factors: list[str] = Field(description="Factors affecting comp")
    competitive_positioning: str = Field(description="below/at/above market")
    recommendation: str = Field(description="Hiring recommendation")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Compensation Benchmarker",
        instructions=[
            "You are a compensation analyst with expertise in tech industry pay.",
            "Provide data-driven salary recommendations.",
            "",
            "Consider these factors:",
            "- Geographic location and cost of living",
            "- Years of experience and seniority level",
            "- Company size and funding stage",
            "- Industry (FinTech typically pays 10-15% above average)",
            "- Current market conditions",
            "",
            "Base your analysis on typical 2024 market data:",
            "- SF/NYC: Premium markets (+20-30%)",
            "- Seattle/Boston/Austin: Strong markets (+10-15%)",
            "- Remote: Usually indexed to national average or location",
            "",
            "Provide actionable recommendations for hiring managers.",
        ],
        output_schema=CompAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Compensation Benchmarker - Demo")
    print("=" * 60)
    
    query = f"""Analyze compensation for:
Role: {config.get('role', DEFAULT_CONFIG['role'])}
Location: {config.get('location', DEFAULT_CONFIG['location'])}
Experience: {config.get('experience_years', DEFAULT_CONFIG['experience_years'])} years
Company: {config.get('company_size', DEFAULT_CONFIG['company_size'])}
Industry: {config.get('industry', DEFAULT_CONFIG['industry'])}"""
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, CompAnalysis):
        print(f"\n💼 {result.role}")
        print(f"📍 {result.location} | {result.experience_level.title()} Level")
        
        sr = result.base_salary_range
        print(f"\n📊 Market Base Salary:")
        print(f"   25th: ${sr.percentile_25:,}")
        print(f"   50th: ${sr.percentile_50:,} (median)")
        print(f"   75th: ${sr.percentile_75:,}")
        print(f"   90th: ${sr.percentile_90:,}")
        
        print(f"\n🎯 Recommended Offer Range:")
        print(f"   ${result.recommended_range_min:,} - ${result.recommended_range_max:,}")
        
        print(f"\n📈 Additional Comp:")
        print(f"   Equity: {result.equity_range}")
        print(f"   Bonus: {result.bonus_typical}")
        print(f"   Total Comp: {result.total_comp_estimate}")
        
        print(f"\n🔍 Market Factors:")
        for f in result.market_factors:
            print(f"   • {f}")
        
        pos_icon = {"below": "⬇️", "at": "➡️", "above": "⬆️"}
        print(f"\n{pos_icon.get(result.competitive_positioning, '?')} Positioning: {result.competitive_positioning.title()} Market")
        print(f"\n💡 {result.recommendation}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Compensation Benchmarker")
    parser.add_argument("--role", "-r", type=str, default=DEFAULT_CONFIG["role"])
    parser.add_argument("--location", "-l", type=str, default=DEFAULT_CONFIG["location"])
    parser.add_argument("--years", "-y", type=int, default=DEFAULT_CONFIG["experience_years"])
    args = parser.parse_args()
    config = {**DEFAULT_CONFIG, "role": args.role, "location": args.location, "experience_years": args.years}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
