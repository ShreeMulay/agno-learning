"""
Example #212: Research Team Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Collaborative research team with specialized roles for comprehensive analysis
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"depth": "standard"}

class ResearchFinding(BaseModel):
    area: str = Field(description="Research area")
    findings: list[str] = Field(description="Key findings")
    confidence: str = Field(description="high, medium, low")
    sources_needed: list[str] = Field(description="Additional sources to verify")

class ResearchReport(BaseModel):
    topic: str = Field(description="Research topic")
    executive_summary: str = Field(description="Brief overview")
    findings: list[ResearchFinding] = Field(description="Findings by area")
    methodology_notes: str = Field(description="How research was conducted")
    gaps_identified: list[str] = Field(description="Knowledge gaps found")
    recommendations: list[str] = Field(description="Action recommendations")
    next_steps: list[str] = Field(description="Suggested follow-up research")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_literature_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Literature Researcher",
        instructions=[
            "You search and analyze existing research and publications.",
            "Identify key studies, papers, and authoritative sources.",
            "Summarize findings from the literature.",
        ],
        markdown=True,
    )

def get_data_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Data Analyst",
        instructions=[
            "You analyze data and statistics related to research topics.",
            "Identify trends, patterns, and quantitative insights.",
            "Provide evidence-based conclusions.",
        ],
        markdown=True,
    )

def get_synthesis_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Research Synthesizer",
        instructions=[
            "You combine findings from multiple research sources.",
            "Create coherent narratives from disparate information.",
            "Identify gaps and recommend further investigation.",
        ],
        output_schema=ResearchReport,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_synthesis_agent(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Research Team - Demo")
    print("=" * 60)
    topic = "The impact of AI on software developer productivity"
    
    lit_agent = get_literature_agent()
    data_agent = get_data_agent()
    synthesizer = agent
    
    print(f"\n📚 Topic: {topic}")
    print("\n🔬 Running research team...")
    
    lit_findings = lit_agent.run(f"Research literature on: {topic}")
    data_findings = data_agent.run(f"Analyze data and statistics on: {topic}")
    
    synthesis_prompt = f"""
    Research Topic: {topic}
    
    Literature Review: {lit_findings.content}
    
    Data Analysis: {data_findings.content}
    
    Synthesize into a comprehensive research report."""
    
    result = synthesizer.run(synthesis_prompt)
    
    if isinstance(result.content, ResearchReport):
        r = result.content
        print(f"\n📋 Executive Summary:\n{r.executive_summary}")
        print(f"\n🔍 Key Findings:")
        for f in r.findings[:3]:
            print(f"  [{f.confidence.upper()}] {f.area}: {f.findings[0] if f.findings else 'N/A'}")
        print(f"\n⚠️ Gaps: {', '.join(r.gaps_identified[:3])}")
        print(f"\n📌 Recommendations:")
        for rec in r.recommendations[:3]:
            print(f"  • {rec}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", "-d", default=DEFAULT_CONFIG["depth"])
    args = parser.parse_args()
    run_demo(get_agent(), {"depth": args.depth})

if __name__ == "__main__": main()
