"""
Example #041: Resume Screener
Category: business/hr

DESCRIPTION:
Parses resumes, matches against job descriptions, and ranks candidates.
Extracts skills, experience, and education to provide fit scores.

PATTERNS:
- Knowledge (JD requirements)
- Structured Output (CandidateAssessment)
- Reasoning (match justification)

ARGUMENTS:
- resume (str): Candidate resume text. Default: sample
- job_description (str): JD to match against. Default: sample
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "resume": """
    SARAH CHEN
    Senior Software Engineer | san.chen@email.com | (555) 123-4567 | LinkedIn: /in/sarahchen
    
    SUMMARY
    8+ years of experience building scalable distributed systems. Expert in Python, Go, 
    and cloud-native architectures. Led teams of 5-8 engineers. Passionate about mentoring.
    
    EXPERIENCE
    
    Tech Corp Inc. | Senior Software Engineer | 2020-Present
    - Designed microservices architecture handling 10M+ requests/day
    - Led migration from monolith to Kubernetes, reducing costs 40%
    - Mentored 5 junior engineers, 3 promoted within 18 months
    - Implemented CI/CD pipelines reducing deployment time from days to hours
    
    StartupXYZ | Software Engineer | 2017-2020
    - Built real-time data pipeline processing 1TB+ daily
    - Developed REST APIs serving 50K concurrent users
    - Introduced code review practices, reducing bugs by 35%
    
    EDUCATION
    M.S. Computer Science, Stanford University, 2017
    B.S. Computer Science, UC Berkeley, 2015
    
    SKILLS
    Languages: Python, Go, Java, SQL
    Cloud: AWS (certified), GCP, Kubernetes, Docker
    Tools: PostgreSQL, Redis, Kafka, Terraform
    """,
    "job_description": """
    Senior Backend Engineer
    
    About the Role:
    We're looking for a Senior Backend Engineer to build scalable APIs and services.
    
    Requirements:
    - 5+ years backend development experience
    - Strong Python or Go skills
    - Experience with cloud platforms (AWS/GCP)
    - Kubernetes and containerization experience
    - Database design (SQL and NoSQL)
    
    Nice to Have:
    - Experience with real-time data processing
    - Team leadership or mentoring experience
    - M.S. in Computer Science
    
    We Offer:
    - Competitive salary $180K-$220K
    - Remote-first culture
    - Equity package
    """,
}


class SkillMatch(BaseModel):
    skill: str = Field(description="Skill name")
    candidate_level: str = Field(description="none/basic/intermediate/expert")
    required_level: str = Field(description="required/preferred/nice-to-have")
    match: bool = Field(description="Does candidate meet requirement")


class CandidateAssessment(BaseModel):
    candidate_name: str = Field(description="Candidate's name")
    years_experience: int = Field(description="Total years of relevant experience")
    current_role: str = Field(description="Current/most recent role")
    education_level: str = Field(description="Highest education")
    skill_matches: list[SkillMatch] = Field(description="Skill-by-skill assessment")
    strengths: list[str] = Field(description="Top 3 strengths for this role")
    gaps: list[str] = Field(description="Missing requirements or concerns")
    overall_fit_score: int = Field(ge=0, le=100, description="Overall fit percentage")
    recommendation: str = Field(description="strong_yes/yes/maybe/no")
    reasoning: str = Field(description="Brief justification for recommendation")
    suggested_interview_focus: list[str] = Field(description="Areas to probe in interview")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Resume Screener",
        instructions=[
            "You are an expert technical recruiter and hiring manager.",
            "Evaluate candidates objectively against job requirements.",
            "",
            "Evaluation Process:",
            "1. Extract all skills, experience, and education from resume",
            "2. Map each JD requirement to candidate qualifications",
            "3. Identify gaps and strengths",
            "4. Calculate overall fit score",
            "",
            "Scoring Guide:",
            "90-100: Exceeds all requirements, strong yes",
            "75-89: Meets all requirements, yes",
            "60-74: Meets most requirements, maybe",
            "Below 60: Missing key requirements, no",
            "",
            "Be objective and evidence-based in your assessment.",
        ],
        output_schema=CandidateAssessment,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Resume Screener - Demo")
    print("=" * 60)
    
    resume = config.get("resume", DEFAULT_CONFIG["resume"])
    jd = config.get("job_description", DEFAULT_CONFIG["job_description"])
    
    query = f"""Evaluate this candidate for the role:

JOB DESCRIPTION:
{jd}

RESUME:
{resume}"""
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, CandidateAssessment):
        print(f"\n👤 Candidate: {result.candidate_name}")
        print(f"Experience: {result.years_experience} years | {result.current_role}")
        print(f"Education: {result.education_level}")
        
        print(f"\n📊 Skill Assessment:")
        for sm in result.skill_matches[:5]:
            icon = "✅" if sm.match else "❌"
            print(f"  {icon} {sm.skill}: {sm.candidate_level} (need: {sm.required_level})")
        
        print(f"\n💪 Strengths:")
        for s in result.strengths:
            print(f"  • {s}")
        
        if result.gaps:
            print(f"\n⚠️ Gaps:")
            for g in result.gaps:
                print(f"  • {g}")
        
        rec_icon = {"strong_yes": "🌟", "yes": "✅", "maybe": "🤔", "no": "❌"}
        print(f"\n{rec_icon.get(result.recommendation, '?')} Recommendation: {result.recommendation.upper()}")
        print(f"📈 Fit Score: {result.overall_fit_score}%")
        print(f"💭 {result.reasoning}")
        
        print(f"\n🎯 Interview Focus:")
        for area in result.suggested_interview_focus:
            print(f"  • {area}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Resume Screener")
    parser.add_argument("--resume", "-r", type=str, default=DEFAULT_CONFIG["resume"])
    parser.add_argument("--jd", "-j", type=str, default=DEFAULT_CONFIG["job_description"])
    args = parser.parse_args()
    agent = get_agent(config={"resume": args.resume, "job_description": args.jd})
    run_demo(agent, {"resume": args.resume, "job_description": args.jd})


if __name__ == "__main__":
    main()
