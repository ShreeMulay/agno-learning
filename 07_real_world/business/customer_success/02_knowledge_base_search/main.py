"""
Example #022: Knowledge Base Search
Category: business/customer_success

DESCRIPTION:
Semantic search across help documentation and knowledge base articles.
Understands natural language queries, finds relevant articles, and provides
direct answers with source citations. Supports follow-up questions.

PATTERNS:
- Knowledge (document search and retrieval)
- Memory (conversation context for follow-ups)

ARGUMENTS:
- query (str): User's search query. Default: sample
- kb_context (str): Knowledge base content. Default: sample articles
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "query": "How do I reset my password?",
    "kb_context": """
    KNOWLEDGE BASE ARTICLES:
    
    === Article: Password Reset ===
    ID: KB-001
    Category: Account Management
    
    To reset your password:
    1. Go to the login page
    2. Click "Forgot Password"
    3. Enter your email address
    4. Check your inbox for the reset link (valid for 24 hours)
    5. Click the link and create a new password
    
    Password requirements:
    - At least 12 characters
    - One uppercase letter
    - One number
    - One special character
    
    If you don't receive the email, check your spam folder or contact support.
    
    === Article: Two-Factor Authentication ===
    ID: KB-002
    Category: Security
    
    Setting up 2FA:
    1. Go to Settings > Security
    2. Click "Enable 2FA"
    3. Scan the QR code with your authenticator app
    4. Enter the verification code
    5. Save your backup codes securely
    
    Supported apps: Google Authenticator, Authy, 1Password
    
    === Article: Billing FAQ ===
    ID: KB-003
    Category: Billing
    
    Common billing questions:
    - Invoices are sent on the 1st of each month
    - Payment methods: Credit card, ACH, Wire transfer
    - To update payment info: Settings > Billing > Payment Methods
    - Refund policy: Full refund within 30 days, prorated after
    
    === Article: API Rate Limits ===
    ID: KB-004
    Category: Technical
    
    Rate limits by plan:
    - Free: 100 requests/hour
    - Pro: 1,000 requests/hour
    - Enterprise: 10,000 requests/hour
    
    Rate limit headers:
    - X-RateLimit-Limit: Your limit
    - X-RateLimit-Remaining: Requests left
    - X-RateLimit-Reset: Reset timestamp
    """,
    "product_name": "CloudApp",
}


# =============================================================================
# Output Schema
# =============================================================================

class ArticleMatch(BaseModel):
    """Matched knowledge base article."""
    
    article_id: str = Field(description="Article ID (e.g., KB-001)")
    title: str = Field(description="Article title")
    category: str = Field(description="Article category")
    relevance_score: int = Field(ge=0, le=100, description="Relevance to query 0-100")
    matched_section: str = Field(description="Most relevant section from article")


class DirectAnswer(BaseModel):
    """Direct answer to the query."""
    
    answer: str = Field(description="Clear, concise answer to the question")
    confidence: str = Field(description="high/medium/low confidence in answer")
    source_articles: list[str] = Field(description="Article IDs used for answer")
    steps: list[str] = Field(default_factory=list, description="Step-by-step instructions if applicable")


class KBSearchResult(BaseModel):
    """Complete knowledge base search result."""
    
    query: str = Field(description="Original query")
    query_intent: str = Field(description="Understood intent of the query")
    direct_answer: DirectAnswer = Field(description="Direct answer to query")
    matched_articles: list[ArticleMatch] = Field(description="Relevant articles found")
    related_topics: list[str] = Field(description="Related topics user might want")
    suggested_followups: list[str] = Field(description="Suggested follow-up questions")
    needs_human: bool = Field(description="Whether human support is recommended")
    human_reason: Optional[str] = Field(default=None, description="Why human support needed")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Knowledge Base Search agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for KB search
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Knowledge Base Search",
        instructions=[
            "You are a helpful knowledge base assistant.",
            "Search the documentation to answer user questions accurately.",
            "",
            f"Product: {cfg['product_name']}",
            "",
            "Search Guidelines:",
            "- Understand the user's intent, not just keywords",
            "- Provide direct, actionable answers",
            "- Always cite source articles",
            "- If uncertain, acknowledge limitations",
            "- Suggest related topics for comprehensive help",
            "",
            "Response Quality:",
            "- Be concise but complete",
            "- Use step-by-step format for procedures",
            "- Highlight important warnings or notes",
            "- Recommend human support for complex issues",
            "",
            "Knowledge Base Content:",
            cfg["kb_context"],
        ],
        output_schema=KBSearchResult,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of KB search."""
    print("\n" + "=" * 60)
    print("  Knowledge Base Search - Demo")
    print("=" * 60)
    
    query = config.get("query", DEFAULT_CONFIG["query"])
    
    prompt = f"""
    User Question: {query}
    
    Search the knowledge base and provide the best answer with sources.
    """
    
    print(f"\nQuery: {query}")
    print("-" * 40)
    print("Searching knowledge base...")
    
    response = agent.run(prompt)
    
    # Handle structured output
    result = response.content
    if isinstance(result, KBSearchResult):
        print(f"\n{'='*50}")
        print(f"SEARCH RESULTS")
        print(f"{'='*50}")
        
        print(f"\n🔍 Query: {result.query}")
        print(f"📌 Intent: {result.query_intent}")
        
        da = result.direct_answer
        print(f"\n💬 Answer ({da.confidence} confidence):")
        print(f"  {da.answer}")
        
        if da.steps:
            print(f"\n📋 Steps:")
            for i, step in enumerate(da.steps, 1):
                print(f"  {i}. {step}")
        
        print(f"\n  Sources: {', '.join(da.source_articles)}")
        
        print(f"\n📚 Matched Articles:")
        for article in result.matched_articles:
            print(f"\n  [{article.article_id}] {article.title}")
            print(f"    Category: {article.category} | Relevance: {article.relevance_score}%")
            print(f"    Excerpt: {article.matched_section[:100]}...")
        
        if result.related_topics:
            print(f"\n🔗 Related Topics:")
            for topic in result.related_topics[:3]:
                print(f"  • {topic}")
        
        if result.suggested_followups:
            print(f"\n❓ You might also want to know:")
            for q in result.suggested_followups[:3]:
                print(f"  • {q}")
        
        if result.needs_human:
            print(f"\n⚠️  Human Support Recommended: {result.human_reason}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Knowledge Base Search - Find answers in documentation"
    )
    
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=DEFAULT_CONFIG["query"],
        help="Search query"
    )
    
    args = parser.parse_args()
    
    config = {
        "query": args.query,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
