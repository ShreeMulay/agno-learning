"""
Example #117: Content Adapter
Category: education/teaching
DESCRIPTION: Adapts educational content for different reading levels and needs
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"target_level": "elementary", "accommodation": "none"}

class AdaptedContent(BaseModel):
    original_topic: str = Field(description="Original topic")
    target_level: str = Field(description="Target reading level")
    adapted_text: str = Field(description="Adapted content")
    vocabulary_support: list[str] = Field(description="Key terms with definitions")
    visual_suggestions: list[str] = Field(description="Suggested visuals")
    scaffolding_questions: list[str] = Field(description="Comprehension scaffolds")
    extensions: list[str] = Field(description="Extension activities")
    accommodations_applied: list[str] = Field(description="Accommodations made")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Content Adapter",
        instructions=[
            "Simplify language while maintaining content accuracy",
            "Adjust complexity to target reading level",
            "Provide vocabulary support for key terms",
            "Suggest visual aids and graphic organizers",
            "Apply requested accommodations (ELL, IEP, etc.)"
        ],
        output_schema=AdaptedContent, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Content Adapter - Demo\n" + "=" * 60)
    query = f"""Adapt this content:
Target level: {config['target_level']}
Accommodations: {config['accommodation']}

Original text (high school level):
"Photosynthesis is the biochemical process by which chloroplasts in plant cells 
convert light energy into chemical energy, storing it in glucose molecules. 
This process requires carbon dioxide and water as reactants, and produces 
oxygen as a byproduct. The light-dependent reactions occur in the thylakoid 
membranes, while the Calvin cycle takes place in the stroma." """
    response = agent.run(query)
    result = response.content
    if isinstance(result, AdaptedContent):
        print(f"\nOriginal Topic: {result.original_topic}")
        print(f"Target Level: {result.target_level}")
        print(f"\nAdapted Text:\n{result.adapted_text[:300]}...")
        print(f"\nVocabulary Support:")
        for v in result.vocabulary_support[:3]:
            print(f"  • {v}")
        print(f"\nScaffolding Questions:")
        for q in result.scaffolding_questions[:2]:
            print(f"  ? {q}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-level", "-l", default=DEFAULT_CONFIG["target_level"])
    parser.add_argument("--accommodation", "-a", default=DEFAULT_CONFIG["accommodation"])
    args = parser.parse_args()
    run_demo(get_agent(), {"target_level": args.target_level, "accommodation": args.accommodation})

if __name__ == "__main__": main()
