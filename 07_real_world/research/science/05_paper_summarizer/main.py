"""
Example #175: Paper Summarizer Agent
Category: research/science
DESCRIPTION: Summarizes scientific papers in structured format
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"paper_type": "empirical", "audience": "researcher", "detail_level": "comprehensive"}

class PaperSummaryResult(BaseModel):
    title: str = Field(description="Paper title")
    authors: str = Field(description="Authors")
    publication: str = Field(description="Journal/venue")
    research_question: str = Field(description="Main research question")
    methodology: str = Field(description="Methodology summary")
    key_findings: list[str] = Field(description="Key findings")
    contributions: list[str] = Field(description="Main contributions")
    limitations: list[str] = Field(description="Stated limitations")
    future_work: list[str] = Field(description="Suggested future work")
    critical_assessment: str = Field(description="Critical assessment")
    relevance_to_field: str = Field(description="Relevance to field")
    one_sentence_summary: str = Field(description="One sentence summary")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Paper Summarizer",
        instructions=[
            "You are an expert scientific paper summarizer.",
            f"Summarize {cfg['paper_type']} papers for {cfg['audience']} audience",
            f"Provide {cfg['detail_level']} summaries",
            "Extract key methodological details",
            "Identify main contributions and limitations",
            "Provide critical assessment",
        ],
        output_schema=PaperSummaryResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Paper Summarizer Agent - Demo")
    print("=" * 60)
    sample_abstract = """This study investigates the effect of mindfulness meditation on stress 
reduction in healthcare workers. A randomized controlled trial with 150 participants showed 
significant reduction in cortisol levels (p<0.01) after 8 weeks of daily practice. Results 
suggest mindfulness as an effective intervention for occupational stress."""
    query = f"""Summarize this paper for {config['audience']} audience:

Abstract: {sample_abstract}

Create {config['detail_level']} summary of this {config['paper_type']} paper."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PaperSummaryResult):
        print(f"\n📄 {result.title}")
        print(f"👤 {result.authors}")
        print(f"\n❓ Question: {result.research_question}")
        print(f"🔬 Method: {result.methodology}")
        print(f"\n💡 Key Findings:")
        for f in result.key_findings[:3]:
            print(f"  • {f}")
        print(f"\n⚠️ Limitations: {', '.join(result.limitations[:2])}")
        print(f"\n📝 TL;DR: {result.one_sentence_summary}")

def main():
    parser = argparse.ArgumentParser(description="Paper Summarizer Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["paper_type"])
    parser.add_argument("--audience", "-a", default=DEFAULT_CONFIG["audience"])
    parser.add_argument("--detail", "-d", default=DEFAULT_CONFIG["detail_level"])
    args = parser.parse_args()
    config = {"paper_type": args.type, "audience": args.audience, "detail_level": args.detail}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
