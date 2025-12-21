"""
Example #141: Product Cataloger Agent
Category: industry/ecommerce
DESCRIPTION: Generates product catalog entries with descriptions and metadata
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"product_name": "Wireless Bluetooth Headphones", "category": "Electronics"}

class ProductCatalogEntry(BaseModel):
    title: str = Field(description="SEO-optimized product title")
    description: str = Field(description="Compelling product description")
    bullet_points: list[str] = Field(description="Key feature bullet points")
    category_path: str = Field(description="Category hierarchy path")
    tags: list[str] = Field(description="Search and filter tags")
    specifications: dict = Field(description="Technical specifications")
    seo_keywords: list[str] = Field(description="SEO keywords")
    target_audience: str = Field(description="Primary target audience")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Product Cataloger",
        instructions=[
            "You are an expert e-commerce product copywriter and catalog manager.",
            f"Create catalog entries for the {cfg['category']} category",
            "Write compelling, SEO-optimized product descriptions",
            "Include accurate specifications and feature highlights",
            "Use persuasive language that drives conversions",
            "Ensure consistency with e-commerce best practices",
        ],
        output_schema=ProductCatalogEntry,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Product Cataloger Agent - Demo")
    print("=" * 60)
    query = f"""Create a product catalog entry for:
- Product: {config['product_name']}
- Category: {config['category']}

Generate title, description, specs, and metadata."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ProductCatalogEntry):
        print(f"\n📦 Title: {result.title}")
        print(f"📁 Category: {result.category_path}")
        print(f"\n📝 Description:\n{result.description[:200]}...")
        print(f"\n⭐ Features:")
        for bp in result.bullet_points[:4]:
            print(f"  • {bp}")
        print(f"\n🏷️ Tags: {', '.join(result.tags[:5])}")

def main():
    parser = argparse.ArgumentParser(description="Product Cataloger Agent")
    parser.add_argument("--product", "-p", default=DEFAULT_CONFIG["product_name"])
    parser.add_argument("--category", "-c", default=DEFAULT_CONFIG["category"])
    args = parser.parse_args()
    config = {"product_name": args.product, "category": args.category}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
