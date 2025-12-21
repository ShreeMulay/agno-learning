"""
Example #092: Symptom Checker
Category: healthcare/clinical
DESCRIPTION: Analyzes patient symptoms to suggest possible conditions and triage urgency
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"urgency_threshold": "moderate"}

class PossibleCondition(BaseModel):
    condition: str = Field(description="Medical condition name")
    likelihood: str = Field(description="high, moderate, low")
    key_symptoms: list[str] = Field(description="Matching symptoms")
    red_flags: list[str] = Field(description="Warning signs present")

class SymptomAnalysis(BaseModel):
    presenting_symptoms: list[str] = Field(description="Reported symptoms")
    duration: str = Field(description="Symptom duration")
    triage_level: str = Field(description="emergent, urgent, routine")
    possible_conditions: list[PossibleCondition] = Field(description="Differential")
    recommended_tests: list[str] = Field(description="Suggested workup")
    follow_up_questions: list[str] = Field(description="Additional history needed")
    disclaimer: str = Field(description="Medical disclaimer")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Symptom Checker",
        instructions=[
            "Analyze reported symptoms systematically",
            "Generate differential diagnosis with likelihood",
            "Identify red flag symptoms requiring urgent care",
            "Suggest appropriate diagnostic workup",
            "Always include medical disclaimer - not a substitute for professional evaluation"
        ],
        output_schema=SymptomAnalysis, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Symptom Checker - Demo\n" + "=" * 60)
    query = """Analyze these symptoms:
- Severe headache for 3 days
- Stiff neck
- Sensitivity to light
- Low-grade fever (100.4F)
- No recent head trauma
- 32-year-old female, generally healthy"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SymptomAnalysis):
        print(f"\nTriage Level: {result.triage_level.upper()}")
        print(f"Duration: {result.duration}")
        print(f"\nPossible Conditions:")
        for c in result.possible_conditions[:3]:
            print(f"  [{c.likelihood}] {c.condition}")
            if c.red_flags:
                print(f"    ⚠️ Red flags: {', '.join(c.red_flags)}")
        print(f"\nRecommended Tests: {', '.join(result.recommended_tests[:3])}")
        print(f"\nDisclaimer: {result.disclaimer[:150]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--urgency-threshold", "-u", default=DEFAULT_CONFIG["urgency_threshold"])
    args = parser.parse_args()
    run_demo(get_agent(), {"urgency_threshold": args.urgency_threshold})

if __name__ == "__main__": main()
