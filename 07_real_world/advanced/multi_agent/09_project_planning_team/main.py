"""
Example #219: Project Planning Team Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Cross-functional planning with product, engineering, and design perspectives
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"methodology": "agile"}

class Milestone(BaseModel):
    name: str = Field(description="Milestone name")
    duration: str = Field(description="Estimated duration")
    dependencies: list[str] = Field(description="What must complete first")
    deliverables: list[str] = Field(description="What will be delivered")

class ProjectPlan(BaseModel):
    project_name: str = Field(description="Project name")
    objective: str = Field(description="Primary goal")
    scope: list[str] = Field(description="What's in scope")
    out_of_scope: list[str] = Field(description="Explicitly excluded")
    milestones: list[Milestone] = Field(description="Project milestones")
    total_duration: str = Field(description="Estimated total time")
    team_requirements: list[str] = Field(description="Required team members")
    risks: list[str] = Field(description="Key project risks")
    success_criteria: list[str] = Field(description="How success is measured")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_product_manager(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Product Manager",
        instructions=[
            "You define product requirements and priorities.",
            "Focus on user value and business goals.",
            "Balance scope with timeline.",
        ],
        markdown=True,
    )

def get_tech_lead(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Technical Lead",
        instructions=[
            "You assess technical feasibility and architecture.",
            "Estimate engineering effort.",
            "Identify technical risks and dependencies.",
        ],
        markdown=True,
    )

def get_project_manager(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Project Manager",
        instructions=[
            "You create comprehensive project plans.",
            "Balance all stakeholder inputs.",
            "Define realistic timelines and milestones.",
            "Identify risks and mitigation strategies.",
        ],
        output_schema=ProjectPlan,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_project_manager(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Project Planning Team - Demo")
    print("=" * 60)
    
    project_brief = """
    Project: Customer Dashboard Redesign
    Goal: Modernize the customer dashboard with improved UX and new analytics features
    Constraints: Must maintain backward compatibility, 3-month deadline
    Resources: 2 frontend devs, 1 backend dev, 1 designer"""
    
    pm = get_product_manager()
    tech_lead = get_tech_lead()
    project_mgr = agent
    
    print(f"\n📋 Planning: Customer Dashboard Redesign")
    
    product_input = pm.run(f"Define product requirements for:\n{project_brief}")
    tech_input = tech_lead.run(f"Assess technical approach for:\n{project_brief}")
    
    plan_prompt = f"""
    Project Brief: {project_brief}
    
    Product Requirements: {product_input.content}
    Technical Assessment: {tech_input.content}
    
    Create comprehensive project plan using {config.get('methodology', 'agile')} methodology."""
    
    result = project_mgr.run(plan_prompt)
    
    if isinstance(result.content, ProjectPlan):
        r = result.content
        print(f"\n🎯 Objective: {r.objective}")
        print(f"⏱️ Duration: {r.total_duration}")
        print(f"\n📍 Milestones:")
        for m in r.milestones:
            print(f"  • {m.name} ({m.duration})")
        print(f"\n👥 Team Needed: {', '.join(r.team_requirements)}")
        print(f"\n⚠️ Risks:")
        for risk in r.risks[:3]:
            print(f"  • {risk}")
        print(f"\n✅ Success Criteria:")
        for criteria in r.success_criteria:
            print(f"  • {criteria}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--methodology", "-m", default=DEFAULT_CONFIG["methodology"])
    args = parser.parse_args()
    run_demo(get_agent(), {"methodology": args.methodology})

if __name__ == "__main__": main()
