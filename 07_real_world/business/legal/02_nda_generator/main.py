"""
Example #052: NDA Generator
Category: business/legal

DESCRIPTION:
Generates customized Non-Disclosure Agreements based on
party details and specific requirements.

PATTERNS:
- Structured Output (NDADocument)
- Knowledge (NDA best practices)

ARGUMENTS:
- disclosing_party (str): Party sharing confidential info
- receiving_party (str): Party receiving info
- purpose (str): Purpose of disclosure
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "disclosing_party": "TechStartup Inc., a Delaware corporation",
    "receiving_party": "Investor Partners LLC, a New York limited liability company",
    "purpose": "Evaluation of potential investment in TechStartup",
    "mutual": False,
    "duration_years": 3,
    "governing_state": "Delaware",
}


class NDADocument(BaseModel):
    title: str = Field(description="Document title")
    preamble: str = Field(description="Opening paragraph with parties")
    recitals: str = Field(description="Whereas clauses explaining purpose")
    definition_of_confidential: str = Field(description="What counts as confidential")
    exclusions: list[str] = Field(description="What's excluded from confidential")
    obligations: list[str] = Field(description="Receiving party obligations")
    permitted_disclosures: list[str] = Field(description="When disclosure is allowed")
    term_clause: str = Field(description="Duration and survival")
    return_of_materials: str = Field(description="What happens to materials")
    remedies_clause: str = Field(description="Remedies for breach")
    general_provisions: list[str] = Field(description="Boilerplate clauses")
    signature_block: str = Field(description="Signature section")
    is_mutual: bool = Field(description="Is this mutual NDA?")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="NDA Generator",
        instructions=[
            "You are a corporate attorney drafting NDAs.",
            "Generate clear, enforceable confidentiality agreements.",
            "",
            f"Parameters:",
            f"- Disclosing Party: {cfg['disclosing_party']}",
            f"- Receiving Party: {cfg['receiving_party']}",
            f"- Purpose: {cfg['purpose']}",
            f"- Mutual: {cfg['mutual']}",
            f"- Duration: {cfg['duration_years']} years",
            f"- Governing Law: {cfg['governing_state']}",
            "",
            "Key Elements:",
            "- Clear definition of confidential information",
            "- Reasonable exclusions (public info, prior knowledge)",
            "- Standard of care (reasonable efforts)",
            "- Permitted disclosures (legal requirements, employees)",
            "- Return/destruction of materials",
            "- Injunctive relief clause",
        ],
        output_schema=NDADocument,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  NDA Generator - Demo")
    print("=" * 60)
    
    query = f"""Generate an NDA for:
Disclosing Party: {config.get('disclosing_party', DEFAULT_CONFIG['disclosing_party'])}
Receiving Party: {config.get('receiving_party', DEFAULT_CONFIG['receiving_party'])}
Purpose: {config.get('purpose', DEFAULT_CONFIG['purpose'])}"""
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, NDADocument):
        print(f"\n{'='*60}")
        print(f"{result.title}")
        print(f"{'='*60}")
        
        print(f"\n{result.preamble}")
        print(f"\n{result.recitals}")
        
        print(f"\n1. CONFIDENTIAL INFORMATION")
        print(f"{result.definition_of_confidential}")
        
        print(f"\nExclusions:")
        for e in result.exclusions:
            print(f"   • {e}")
        
        print(f"\n2. OBLIGATIONS")
        for o in result.obligations:
            print(f"   • {o}")
        
        print(f"\n3. PERMITTED DISCLOSURES")
        for p in result.permitted_disclosures:
            print(f"   • {p}")
        
        print(f"\n4. TERM")
        print(f"{result.term_clause}")
        
        print(f"\n5. RETURN OF MATERIALS")
        print(f"{result.return_of_materials}")
        
        print(f"\n6. REMEDIES")
        print(f"{result.remedies_clause}")
        
        print(f"\n7. GENERAL PROVISIONS")
        for g in result.general_provisions:
            print(f"   • {g}")
        
        print(f"\n{result.signature_block}")
        print(f"\n[{'Mutual' if result.is_mutual else 'One-Way'} NDA]")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="NDA Generator")
    parser.add_argument("--disclosing", "-d", type=str, default=DEFAULT_CONFIG["disclosing_party"])
    parser.add_argument("--receiving", "-r", type=str, default=DEFAULT_CONFIG["receiving_party"])
    parser.add_argument("--purpose", "-p", type=str, default=DEFAULT_CONFIG["purpose"])
    args = parser.parse_args()
    config = {"disclosing_party": args.disclosing, "receiving_party": args.receiving, "purpose": args.purpose}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
