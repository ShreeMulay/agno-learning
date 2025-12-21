"""
Example #096: Lab Interpreter
Category: healthcare/clinical
DESCRIPTION: Interprets laboratory results with clinical context and recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"panel_type": "comprehensive"}

class LabResult(BaseModel):
    test: str = Field(description="Test name")
    value: str = Field(description="Result value")
    reference: str = Field(description="Reference range")
    status: str = Field(description="normal, high, low, critical")
    interpretation: str = Field(description="Clinical meaning")

class LabInterpretation(BaseModel):
    panel_type: str = Field(description="Type of panel")
    critical_values: list[LabResult] = Field(description="Critical/urgent findings")
    abnormal_results: list[LabResult] = Field(description="Abnormal findings")
    clinical_patterns: list[str] = Field(description="Patterns suggesting diagnoses")
    differential_diagnoses: list[str] = Field(description="Conditions to consider")
    recommended_actions: list[str] = Field(description="Follow-up actions")
    additional_tests: list[str] = Field(description="Additional workup needed")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Lab Interpreter",
        instructions=[
            "Interpret laboratory results in clinical context",
            "Identify critical values requiring immediate action",
            "Recognize patterns suggesting specific diagnoses",
            "Provide differential based on lab patterns",
            "Recommend follow-up testing and actions"
        ],
        output_schema=LabInterpretation, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Lab Interpreter - Demo\n" + "=" * 60)
    query = f"""Interpret this {config['panel_type']} metabolic panel:

Patient: 55yo F with fatigue and polyuria

Results:
- Glucose: 342 mg/dL (70-100)
- BUN: 38 mg/dL (7-20)
- Creatinine: 1.8 mg/dL (0.6-1.2)
- Sodium: 128 mEq/L (136-145)
- Potassium: 5.8 mEq/L (3.5-5.0)
- CO2: 18 mEq/L (23-29)
- Anion gap: 16 (8-12)
- HbA1c: 12.1% (<5.7%)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LabInterpretation):
        print(f"\nPanel: {result.panel_type}")
        print(f"\n🚨 Critical Values ({len(result.critical_values)}):")
        for c in result.critical_values:
            print(f"  - {c.test}: {c.value} ({c.reference})")
        print(f"\nClinical Patterns:")
        for p in result.clinical_patterns:
            print(f"  • {p}")
        print(f"\nDifferential: {', '.join(result.differential_diagnoses[:3])}")
        print(f"\nRecommended Actions:")
        for a in result.recommended_actions[:3]:
            print(f"  → {a}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel-type", "-p", default=DEFAULT_CONFIG["panel_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"panel_type": args.panel_type})

if __name__ == "__main__": main()
