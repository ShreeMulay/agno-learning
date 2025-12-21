"""
Example #220: Quality Assurance Team Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Comprehensive QA with functional, performance, and security testing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"coverage_target": "comprehensive"}

class TestResult(BaseModel):
    test_type: str = Field(description="Type of testing")
    tests_run: int = Field(description="Number of tests executed")
    passed: int = Field(description="Tests passed")
    failed: int = Field(description="Tests failed")
    critical_issues: list[str] = Field(description="Critical bugs found")

class QAReport(BaseModel):
    feature_name: str = Field(description="Feature being tested")
    overall_status: str = Field(description="pass, fail, conditional_pass")
    quality_score: int = Field(description="Quality score 1-100")
    test_results: list[TestResult] = Field(description="Results by test type")
    blocking_issues: list[str] = Field(description="Issues that block release")
    known_issues: list[str] = Field(description="Issues to document")
    release_recommendation: str = Field(description="Release decision and conditions")
    regression_risk: str = Field(description="low, medium, high")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_functional_tester(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Functional Tester",
        instructions=[
            "You perform functional testing of features.",
            "Verify requirements are met.",
            "Test edge cases and error handling.",
        ],
        markdown=True,
    )

def get_performance_tester(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Performance Tester",
        instructions=[
            "You test performance and scalability.",
            "Measure response times and throughput.",
            "Identify bottlenecks and resource issues.",
        ],
        markdown=True,
    )

def get_qa_lead(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="QA Lead",
        instructions=[
            "You synthesize all testing results.",
            "Make release readiness decisions.",
            "Prioritize issues by severity.",
            "Provide clear quality assessment.",
        ],
        output_schema=QAReport,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_qa_lead(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Quality Assurance Team - Demo")
    print("=" * 60)
    
    feature = """
    Feature: New User Registration Flow
    Changes:
    - Redesigned registration form
    - Added social login (Google, GitHub)
    - Improved email verification
    - New password strength requirements
    Environment: Staging
    Sprint: 2024-Q1-S3"""
    
    functional = get_functional_tester()
    performance = get_performance_tester()
    qa_lead = agent
    
    print(f"\n🧪 Testing: New User Registration Flow")
    
    func_results = functional.run(f"Functional test this feature:\n{feature}")
    perf_results = performance.run(f"Performance test this feature:\n{feature}")
    
    report_prompt = f"""
    Feature Under Test: {feature}
    
    Functional Testing: {func_results.content}
    Performance Testing: {perf_results.content}
    
    Coverage Target: {config.get('coverage_target', 'comprehensive')}
    
    Generate QA report and release recommendation."""
    
    result = qa_lead.run(report_prompt)
    
    if isinstance(result.content, QAReport):
        r = result.content
        status_emoji = "✅" if r.overall_status == "pass" else "⚠️" if r.overall_status == "conditional_pass" else "❌"
        print(f"\n{status_emoji} Status: {r.overall_status.upper()}")
        print(f"📊 Quality Score: {r.quality_score}/100")
        print(f"⚡ Regression Risk: {r.regression_risk}")
        
        if r.blocking_issues:
            print(f"\n🔴 Blocking Issues:")
            for issue in r.blocking_issues:
                print(f"  • {issue}")
        
        print(f"\n📋 Test Results:")
        for tr in r.test_results:
            print(f"  {tr.test_type}: {tr.passed}/{tr.tests_run} passed")
        
        print(f"\n🚀 Release Recommendation: {r.release_recommendation}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-target", "-c", default=DEFAULT_CONFIG["coverage_target"])
    args = parser.parse_args()
    run_demo(get_agent(), {"coverage_target": args.coverage_target})

if __name__ == "__main__": main()
