"""
Example #056: Legal Document Summarizer
Category: business/legal

DESCRIPTION:
Summarizes complex legal documents into plain language,
highlighting key terms and obligations.

PATTERNS:
- Structured Output (DocumentSummary)
- Reasoning (plain language translation)

ARGUMENTS:
- document (str): Legal document to summarize
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "document": """
    TERMS OF SERVICE
    
    1. ACCEPTANCE OF TERMS
    By accessing or using the Services, you agree to be bound by these Terms. If you
    do not agree, you may not use the Services. We reserve the right to modify these
    Terms at any time, and such modifications shall be effective immediately upon posting.
    
    2. LICENSE GRANT
    Subject to these Terms, we grant you a limited, non-exclusive, non-transferable,
    revocable license to access and use the Services for your personal, non-commercial
    purposes. This license does not include any rights to: (a) modify or copy the
    Services; (b) use the Services for commercial purposes; (c) reverse engineer any
    software; (d) remove any proprietary notices.
    
    3. USER CONTENT
    You retain ownership of content you submit. By submitting content, you grant us a
    worldwide, perpetual, irrevocable, royalty-free license to use, reproduce, modify,
    publish, and distribute such content in any media. You represent that you have all
    rights to grant this license.
    
    4. DISCLAIMER OF WARRANTIES
    THE SERVICES ARE PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR
    IMPLIED. WE DISCLAIM ALL WARRANTIES INCLUDING MERCHANTABILITY, FITNESS FOR A
    PARTICULAR PURPOSE, AND NON-INFRINGEMENT. WE DO NOT WARRANT THAT THE SERVICES
    WILL BE UNINTERRUPTED OR ERROR-FREE.
    
    5. LIMITATION OF LIABILITY
    IN NO EVENT SHALL WE BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL,
    OR PUNITIVE DAMAGES. OUR TOTAL LIABILITY SHALL NOT EXCEED THE AMOUNTS PAID BY YOU
    IN THE TWELVE MONTHS PRECEDING THE CLAIM.
    
    6. ARBITRATION
    Any dispute shall be resolved through binding arbitration in accordance with the
    AAA Commercial Arbitration Rules. You waive any right to participate in class actions.
    """,
}


class KeyTerm(BaseModel):
    term: str = Field(description="The legal term or clause")
    plain_language: str = Field(description="What it means in simple terms")
    impact: str = Field(description="favorable/neutral/unfavorable for user")
    importance: str = Field(description="high/medium/low")


class DocumentSummary(BaseModel):
    document_type: str = Field(description="Type of legal document")
    parties: list[str] = Field(description="Parties involved")
    effective_date: Optional[str] = Field(default=None, description="When it takes effect")
    one_sentence_summary: str = Field(description="TL;DR in one sentence")
    key_terms: list[KeyTerm] = Field(description="Important terms explained")
    your_obligations: list[str] = Field(description="What you must do")
    their_obligations: list[str] = Field(description="What they must do")
    your_rights: list[str] = Field(description="What you can do")
    risks_to_know: list[str] = Field(description="Potential downsides")
    unusual_clauses: list[str] = Field(description="Non-standard or concerning terms")
    questions_to_ask: list[str] = Field(description="Clarifications needed")
    reading_time: str = Field(description="Original reading time estimate")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Legal Document Summarizer",
        instructions=[
            "You are a legal document translator specializing in plain language.",
            "Make complex legal documents understandable for non-lawyers.",
            "",
            "Guidelines:",
            "- Use simple, everyday words",
            "- Explain legal jargon",
            "- Highlight what matters most to the reader",
            "- Flag anything unusual or one-sided",
            "- Be accurate - don't oversimplify important nuances",
            "",
            "Common Terms to Translate:",
            "- 'Indemnify' = protect and pay for claims against",
            "- 'Perpetual license' = forever permission",
            "- 'Waive' = give up a right",
            "- 'Binding arbitration' = must use private judge, no court",
        ],
        output_schema=DocumentSummary,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Legal Document Summarizer - Demo")
    print("=" * 60)
    
    document = config.get("document", DEFAULT_CONFIG["document"])
    
    response = agent.run(f"Summarize this legal document:\n\n{document}")
    result = response.content
    
    if isinstance(result, DocumentSummary):
        print(f"\n📄 {result.document_type}")
        print(f"⏱️ Original would take: {result.reading_time}")
        
        print(f"\n📝 TL;DR: {result.one_sentence_summary}")
        
        print(f"\n🔑 Key Terms Explained:")
        for t in result.key_terms:
            imp_icon = {"favorable": "✅", "neutral": "➖", "unfavorable": "⚠️"}
            print(f"\n   {imp_icon.get(t.impact, '?')} {t.term}")
            print(f"   Means: {t.plain_language}")
        
        print(f"\n📋 Your Obligations:")
        for o in result.your_obligations:
            print(f"   • {o}")
        
        print(f"\n✅ Your Rights:")
        for r in result.your_rights:
            print(f"   • {r}")
        
        print(f"\n⚠️ Risks to Know:")
        for r in result.risks_to_know:
            print(f"   • {r}")
        
        if result.unusual_clauses:
            print(f"\n🚨 Unusual Clauses:")
            for u in result.unusual_clauses:
                print(f"   • {u}")
        
        if result.questions_to_ask:
            print(f"\n❓ Questions to Ask:")
            for q in result.questions_to_ask:
                print(f"   • {q}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Legal Document Summarizer")
    parser.add_argument("--document", "-d", type=str, default=DEFAULT_CONFIG["document"])
    args = parser.parse_args()
    agent = get_agent(config={"document": args.document})
    run_demo(agent, {"document": args.document})


if __name__ == "__main__":
    main()
