"""
Example #060: E-Discovery Assistant
Category: business/legal

DESCRIPTION:
Assists with e-discovery by analyzing documents for relevance,
privilege, and key information in litigation contexts.

PATTERNS:
- Reasoning (relevance assessment)
- Structured Output (DocumentReview)

ARGUMENTS:
- document (str): Document to review
- case_context (str): Litigation context
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "document": """
    From: john.smith@acmecorp.com
    To: sarah.legal@acmecorp.com
    CC: mike.ceo@acmecorp.com
    Date: March 15, 2024
    Subject: RE: Vendor Contract Issues
    
    Sarah,
    
    Following up on our call about the DataTech contract dispute. I've reviewed
    the original agreement and there's definitely ambiguity in Section 4.2 about
    the delivery timeline.
    
    I spoke with Mike and we agreed we should try to settle this quietly. The
    last thing we need is for our other vendors to see us in a contract dispute.
    Can you reach out to their counsel and see if they'd consider mediation?
    
    Also, can you check if this email chain is privileged? I want to make sure
    we can speak freely about our strategy.
    
    Between us, I think we have some exposure here. The project manager did
    promise them an extension verbally, though nothing was in writing.
    
    Let me know next steps.
    
    John
    VP, Operations
    """,
    "case_context": "Contract dispute with DataTech Inc. regarding software delivery delays. DataTech is claiming breach of contract and seeking $500K in damages.",
}


class DocumentReview(BaseModel):
    document_type: str = Field(description="Type of document")
    date: str = Field(description="Document date")
    author: str = Field(description="Who created it")
    recipients: list[str] = Field(description="Who received it")
    relevance_score: int = Field(ge=0, le=100, description="Relevance to case")
    relevance_explanation: str = Field(description="Why relevant/not relevant")
    privilege_status: str = Field(description="privileged/not privileged/partial/unclear")
    privilege_basis: str = Field(description="Basis for privilege determination")
    key_admissions: list[str] = Field(description="Potentially damaging statements")
    key_facts: list[str] = Field(description="Important factual information")
    persons_mentioned: list[str] = Field(description="People referenced")
    follow_up_needed: list[str] = Field(description="Additional documents to find")
    production_recommendation: str = Field(description="produce/withhold/redact")
    flags: list[str] = Field(description="Special considerations")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="E-Discovery Assistant",
        instructions=[
            "You are a litigation support specialist reviewing documents.",
            f"Case Context: {cfg['case_context']}",
            "",
            "Review Framework:",
            "- Relevance: Does it relate to claims/defenses?",
            "- Privilege: Attorney-client? Work product?",
            "- Confidentiality: Business sensitive?",
            "- Hot Documents: Admissions, key evidence?",
            "",
            "Privilege Criteria:",
            "- Attorney-client: Communication with lawyer for legal advice",
            "- Work product: Prepared in anticipation of litigation",
            "- Must be kept confidential to maintain privilege",
            "",
            "Be thorough and flag anything notable.",
        ],
        output_schema=DocumentReview,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  E-Discovery Assistant - Demo")
    print("=" * 60)
    
    document = config.get("document", DEFAULT_CONFIG["document"])
    
    response = agent.run(f"Review this document:\n\n{document}")
    result = response.content
    
    if isinstance(result, DocumentReview):
        print(f"\n📄 {result.document_type}")
        print(f"Date: {result.date} | Author: {result.author}")
        print(f"Recipients: {', '.join(result.recipients)}")
        
        print(f"\n📊 Relevance: {result.relevance_score}%")
        print(f"   {result.relevance_explanation}")
        
        priv_icon = {"privileged": "🔒", "not privileged": "🔓", "partial": "⚠️", "unclear": "❓"}
        print(f"\n{priv_icon.get(result.privilege_status, '?')} Privilege: {result.privilege_status.upper()}")
        print(f"   {result.privilege_basis}")
        
        if result.key_admissions:
            print(f"\n🚨 Key Admissions:")
            for a in result.key_admissions:
                print(f"   • {a}")
        
        print(f"\n📋 Key Facts:")
        for f in result.key_facts:
            print(f"   • {f}")
        
        print(f"\n👥 Persons: {', '.join(result.persons_mentioned)}")
        
        if result.follow_up_needed:
            print(f"\n🔍 Follow Up:")
            for f in result.follow_up_needed:
                print(f"   • {f}")
        
        rec_icon = {"produce": "✅", "withhold": "🔒", "redact": "✂️"}
        print(f"\n{rec_icon.get(result.production_recommendation, '?')} Recommendation: {result.production_recommendation.upper()}")
        
        if result.flags:
            print(f"\n🚩 Flags:")
            for f in result.flags:
                print(f"   • {f}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="E-Discovery Assistant")
    parser.add_argument("--document", "-d", type=str, default=DEFAULT_CONFIG["document"])
    parser.add_argument("--context", "-c", type=str, default=DEFAULT_CONFIG["case_context"])
    args = parser.parse_args()
    config = {"document": args.document, "case_context": args.context}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
