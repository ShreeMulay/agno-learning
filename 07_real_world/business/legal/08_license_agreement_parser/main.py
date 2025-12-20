"""
Example #058: License Agreement Parser
Category: business/legal

DESCRIPTION:
Parses software license agreements to extract permissions,
restrictions, and compatibility information.

PATTERNS:
- Knowledge (open source licenses)
- Structured Output (LicenseAnalysis)

ARGUMENTS:
- license_text (str): License agreement text
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "license_text": """
    MIT License
    
    Copyright (c) 2024 Example Corp
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """,
}


class LicenseAnalysis(BaseModel):
    license_name: str = Field(description="Identified license type")
    spdx_id: str = Field(description="SPDX identifier if known")
    category: str = Field(description="permissive/copyleft/proprietary")
    permissions: list[str] = Field(description="What you CAN do")
    conditions: list[str] = Field(description="What you MUST do")
    limitations: list[str] = Field(description="What you CANNOT do")
    commercial_use: bool = Field(description="Can use commercially?")
    modification_allowed: bool = Field(description="Can modify?")
    distribution_allowed: bool = Field(description="Can distribute?")
    patent_grant: bool = Field(description="Includes patent grant?")
    copyleft: bool = Field(description="Requires derivative works same license?")
    compatible_with: list[str] = Field(description="Compatible licenses")
    incompatible_with: list[str] = Field(description="Incompatible licenses")
    summary: str = Field(description="Plain language summary")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="License Agreement Parser",
        instructions=[
            "You are a software licensing expert.",
            "Parse license agreements and extract key terms.",
            "",
            "Common License Types:",
            "- MIT/BSD: Permissive, minimal restrictions",
            "- Apache 2.0: Permissive with patent grant",
            "- GPL: Strong copyleft, derivatives must be GPL",
            "- LGPL: Weak copyleft, linking exceptions",
            "- AGPL: Network copyleft",
            "- Proprietary: All rights reserved",
            "",
            "Focus on practical implications for developers.",
        ],
        output_schema=LicenseAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  License Agreement Parser - Demo")
    print("=" * 60)
    
    license_text = config.get("license_text", DEFAULT_CONFIG["license_text"])
    
    response = agent.run(f"Parse this license:\n\n{license_text}")
    result = response.content
    
    if isinstance(result, LicenseAnalysis):
        cat_icon = {"permissive": "🟢", "copyleft": "🟡", "proprietary": "🔴"}
        print(f"\n📄 {result.license_name} ({result.spdx_id})")
        print(f"{cat_icon.get(result.category, '?')} Category: {result.category}")
        
        print(f"\n✅ Permissions:")
        for p in result.permissions:
            print(f"   • {p}")
        
        print(f"\n📋 Conditions:")
        for c in result.conditions:
            print(f"   • {c}")
        
        print(f"\n❌ Limitations:")
        for l in result.limitations:
            print(f"   • {l}")
        
        print(f"\n📊 Quick Check:")
        print(f"   Commercial: {'✅' if result.commercial_use else '❌'}")
        print(f"   Modify: {'✅' if result.modification_allowed else '❌'}")
        print(f"   Distribute: {'✅' if result.distribution_allowed else '❌'}")
        print(f"   Patent Grant: {'✅' if result.patent_grant else '❌'}")
        print(f"   Copyleft: {'⚠️' if result.copyleft else '✅ No'}")
        
        print(f"\n🔗 Compatible: {', '.join(result.compatible_with) or 'N/A'}")
        print(f"⚠️ Incompatible: {', '.join(result.incompatible_with) or 'None'}")
        
        print(f"\n📝 {result.summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="License Agreement Parser")
    parser.add_argument("--license", "-l", type=str, default=DEFAULT_CONFIG["license_text"])
    args = parser.parse_args()
    agent = get_agent(config={"license_text": args.license})
    run_demo(agent, {"license_text": args.license})


if __name__ == "__main__":
    main()
