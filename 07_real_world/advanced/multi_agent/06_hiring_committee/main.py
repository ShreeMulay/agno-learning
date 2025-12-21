"""
Example #216: Hiring Committee Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Multiple interviewers evaluate candidates from different perspectives
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"role": "software_engineer"}

class InterviewerAssessment(BaseModel):
    interviewer: str = Field(description="Interviewer role")
    rating: int = Field(description="Rating 1-5")
    strengths: list[str] = Field(description="Candidate strengths observed")
    concerns: list[str] = Field(description="Concerns or gaps")
    recommendation: str = Field(description="hire, no_hire, maybe")

class HiringDecision(BaseModel):
    candidate_summary: str = Field(description="Overview of candidate")
    assessments: list[InterviewerAssessment] = Field(description="Individual assessments")
    overall_rating: float = Field(description="Average rating")
    final_decision: str = Field(description="hire, no_hire, second_round")
    decision_rationale: str = Field(description="Why this decision")
    offer_details: str = Field(description="If hiring, offer recommendations")
    onboarding_notes: list[str] = Field(description="Areas for onboarding focus")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_technical_interviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Technical Interviewer",
        instructions=[
            "You assess technical skills and problem-solving ability.",
            "Evaluate coding proficiency and system design knowledge.",
            "Check for learning ability and technical depth.",
        ],
        markdown=True,
    )

def get_culture_interviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Culture Fit Interviewer",
        instructions=[
            "You assess cultural fit and soft skills.",
            "Evaluate communication, collaboration, and values alignment.",
            "Check for growth mindset and adaptability.",
        ],
        markdown=True,
    )

def get_hiring_manager(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Hiring Manager",
        instructions=[
            "You make final hiring decisions based on committee input.",
            "Balance technical skills with culture fit.",
            "Consider team needs and growth potential.",
            "Make fair, well-reasoned decisions.",
        ],
        output_schema=HiringDecision,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_hiring_manager(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Hiring Committee - Demo")
    print("=" * 60)
    
    candidate = """
    Candidate: Alex Chen
    Role: Senior Software Engineer
    Experience: 6 years
    Technical: Strong Python, good system design, some gaps in distributed systems
    Communication: Clear, asks good questions, collaborative
    Background: Grew from junior to senior at previous company
    References: Strong recommendations from past managers"""
    
    tech_interviewer = get_technical_interviewer()
    culture_interviewer = get_culture_interviewer()
    hiring_manager = agent
    
    print(f"\n👤 Evaluating candidate...")
    
    tech_eval = tech_interviewer.run(f"Evaluate this candidate technically:\n{candidate}")
    culture_eval = culture_interviewer.run(f"Evaluate this candidate for culture fit:\n{candidate}")
    
    decision_prompt = f"""
    Candidate Information: {candidate}
    
    Technical Interview: {tech_eval.content}
    Culture Interview: {culture_eval.content}
    
    Make final hiring decision for Senior Software Engineer role."""
    
    result = hiring_manager.run(decision_prompt)
    
    if isinstance(result.content, HiringDecision):
        r = result.content
        decision_emoji = "✅" if r.final_decision == "hire" else "❌" if r.final_decision == "no_hire" else "🔄"
        print(f"\n{decision_emoji} Decision: {r.final_decision.upper()}")
        print(f"📊 Overall Rating: {r.overall_rating:.1f}/5")
        print(f"\n💭 Rationale: {r.decision_rationale}")
        if r.final_decision == "hire":
            print(f"\n💰 Offer: {r.offer_details}")
            print(f"\n📚 Onboarding Focus:")
            for note in r.onboarding_notes:
                print(f"  • {note}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", "-r", default=DEFAULT_CONFIG["role"])
    args = parser.parse_args()
    run_demo(get_agent(), {"role": args.role})

if __name__ == "__main__": main()
