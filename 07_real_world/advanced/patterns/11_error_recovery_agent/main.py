"""
Example #231: Error Recovery Agent
Category: advanced/patterns
DESCRIPTION: Agent with robust error handling and recovery strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"max_retries": 3}

class ErrorInfo(BaseModel):
    error_type: str = Field(description="Type of error encountered")
    error_message: str = Field(description="Error details")
    recovery_action: str = Field(description="How it was handled")

class RecoveryResult(BaseModel):
    success: bool = Field(description="Whether task succeeded")
    attempts: int = Field(description="Number of attempts made")
    errors_encountered: list[ErrorInfo] = Field(description="Errors and recoveries")
    final_result: str = Field(description="Final output or error state")
    recovery_strategy: str = Field(description="Strategy used for recovery")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Error Recovery Agent",
        instructions=[
            f"You handle errors gracefully with up to {cfg['max_retries']} retries.",
            "Detect when something goes wrong.",
            "Apply appropriate recovery strategies.",
            "Provide clear error information when recovery fails.",
        ],
        output_schema=RecoveryResult,
        use_json_mode=True,
        markdown=True,
    )

def execute_with_recovery(agent: Agent, task: str, max_retries: int) -> RecoveryResult:
    """Execute task with error recovery."""
    errors = []
    for attempt in range(1, max_retries + 1):
        try:
            response = agent.run(f"""
            Task: {task}
            Attempt: {attempt}/{max_retries}
            Previous errors: {errors if errors else 'None'}
            
            Execute the task. If you detect issues, describe your recovery approach.""")
            
            if isinstance(response.content, RecoveryResult):
                return response.content
            else:
                return RecoveryResult(
                    success=True, attempts=attempt, errors_encountered=[],
                    final_result=str(response.content)[:200],
                    recovery_strategy="direct_execution"
                )
        except Exception as e:
            errors.append({"error_type": type(e).__name__, "message": str(e)})
    
    return RecoveryResult(
        success=False, attempts=max_retries,
        errors_encountered=[ErrorInfo(error_type=e["error_type"], error_message=e["message"], 
                          recovery_action="retry") for e in errors],
        final_result="Max retries exceeded",
        recovery_strategy="exhausted_retries"
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Error Recovery Agent - Demo")
    print("=" * 60)
    
    task = "Parse this potentially malformed JSON and extract user info: {'name': 'Alice', age: 30}"
    max_retries = config.get("max_retries", 3)
    
    print(f"\n🔧 Task: {task}")
    print(f"🔄 Max retries: {max_retries}")
    
    result = execute_with_recovery(agent, task, max_retries)
    
    status = "✅" if result.success else "❌"
    print(f"\n{status} Success: {result.success}")
    print(f"🔢 Attempts: {result.attempts}")
    print(f"🛡️ Strategy: {result.recovery_strategy}")
    if result.errors_encountered:
        print(f"⚠️ Errors Handled:")
        for e in result.errors_encountered:
            print(f"  - {e.error_type}: {e.recovery_action}")
    print(f"📋 Result: {result.final_result[:150]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-retries", "-r", type=int, default=DEFAULT_CONFIG["max_retries"])
    args = parser.parse_args()
    run_demo(get_agent(config={"max_retries": args.max_retries}), {"max_retries": args.max_retries})

if __name__ == "__main__": main()
