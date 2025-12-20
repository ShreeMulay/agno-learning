"""
Example #044: Job Description Writer
Category: business/hr

DESCRIPTION:
Transforms role requirements into compelling, inclusive job descriptions
optimized for candidate attraction and SEO.

PATTERNS:
- Structured Output (JobDescription)
- Knowledge (JD best practices)

ARGUMENTS:
- role_requirements (str): Basic role info and requirements
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "role_requirements": """
    Role: Senior Data Engineer
    Team: Data Platform
    Location: Remote (US)
    
    Need someone who can:
    - Build data pipelines
    - Work with Spark and Airflow
    - Design data warehouse schemas
    - Mentor junior engineers
    
    Requirements:
    - 5+ years experience
    - Python, SQL
    - Cloud experience (AWS preferred)
    
    Nice to have:
    - dbt experience
    - Real-time streaming
    
    Salary: $160K-$200K
    """,
}


class JobDescription(BaseModel):
    title: str = Field(description="Optimized job title")
    tagline: str = Field(description="One-line hook (max 100 chars)")
    about_company: str = Field(description="Company/team overview paragraph")
    role_summary: str = Field(description="What you'll do paragraph")
    responsibilities: list[str] = Field(description="Key responsibilities (5-7)")
    required_qualifications: list[str] = Field(description="Must-have requirements")
    preferred_qualifications: list[str] = Field(description="Nice-to-have items")
    benefits_highlights: list[str] = Field(description="Top benefits to mention")
    compensation_statement: str = Field(description="Salary/benefits statement")
    inclusive_language_score: int = Field(ge=0, le=100, description="Inclusivity score")
    seo_keywords: list[str] = Field(description="Keywords for job board SEO")
    word_count: int = Field(description="Total word count")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Job Description Writer",
        instructions=[
            "You are an expert talent acquisition copywriter.",
            "Write compelling, inclusive job descriptions that attract top talent.",
            "",
            "Best Practices:",
            "- Lead with impact, not requirements",
            "- Use 'you' language to help candidates see themselves",
            "- Avoid gendered language and jargon",
            "- Keep requirements realistic (no 10 years React)",
            "- Include salary range for transparency",
            "- Highlight growth and learning opportunities",
            "",
            "Structure:",
            "- Hook them with an exciting opener",
            "- Show the impact they'll have",
            "- Be specific about day-to-day work",
            "- Keep total length 400-600 words",
            "",
            "Avoid: 'rockstar', 'ninja', 'guru', 'crushing it'",
        ],
        output_schema=JobDescription,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Job Description Writer - Demo")
    print("=" * 60)
    
    requirements = config.get("role_requirements", DEFAULT_CONFIG["role_requirements"])
    
    response = agent.run(f"Write a job description for:\n\n{requirements}")
    result = response.content
    
    if isinstance(result, JobDescription):
        print(f"\n📝 {result.title}")
        print(f"   {result.tagline}")
        
        print(f"\n🏢 About Us:")
        print(f"   {result.about_company}")
        
        print(f"\n🎯 The Role:")
        print(f"   {result.role_summary}")
        
        print(f"\n📋 Responsibilities:")
        for r in result.responsibilities:
            print(f"   • {r}")
        
        print(f"\n✅ Requirements:")
        for r in result.required_qualifications:
            print(f"   • {r}")
        
        print(f"\n⭐ Nice to Have:")
        for p in result.preferred_qualifications:
            print(f"   • {p}")
        
        print(f"\n💰 {result.compensation_statement}")
        
        print(f"\n🎁 Benefits: {', '.join(result.benefits_highlights[:3])}")
        print(f"\n📊 Stats: {result.word_count} words | Inclusivity: {result.inclusive_language_score}%")
        print(f"🔍 SEO: {', '.join(result.seo_keywords[:5])}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Job Description Writer")
    parser.add_argument("--requirements", "-r", type=str, default=DEFAULT_CONFIG["role_requirements"])
    args = parser.parse_args()
    agent = get_agent(config={"role_requirements": args.requirements})
    run_demo(agent, {"role_requirements": args.requirements})


if __name__ == "__main__":
    main()
