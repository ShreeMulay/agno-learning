"""
Example #230: Async Agent
Category: advanced/patterns
DESCRIPTION: Agent with async execution for concurrent operations
"""
import argparse
import asyncio
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"concurrency": 3}

class AsyncTaskResult(BaseModel):
    task_id: str = Field(description="Task identifier")
    result: str = Field(description="Task result")
    duration_ms: int = Field(description="Execution time")

class AsyncBatchResult(BaseModel):
    total_tasks: int = Field(description="Number of tasks processed")
    successful: int = Field(description="Tasks completed successfully")
    failed: int = Field(description="Tasks that failed")
    results: list[AsyncTaskResult] = Field(description="Individual results")
    total_time: str = Field(description="Total batch time")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Async Agent",
        instructions=[
            f"You handle tasks with concurrency level {cfg['concurrency']}.",
            "Process requests efficiently.",
            "Return structured results.",
        ],
        markdown=True,
    )

async def process_task(agent: Agent, task: str, task_id: str) -> dict:
    """Process a single task asynchronously."""
    import time
    start = time.time()
    # Use sync run in executor for demo (real async would use arun)
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, agent.run, task)
    duration = int((time.time() - start) * 1000)
    return {"task_id": task_id, "result": str(response.content)[:100], "duration_ms": duration}

async def run_batch(agent: Agent, tasks: list[tuple[str, str]], concurrency: int) -> list[dict]:
    """Run multiple tasks with limited concurrency."""
    semaphore = asyncio.Semaphore(concurrency)
    
    async def bounded_task(task: str, task_id: str):
        async with semaphore:
            return await process_task(agent, task, task_id)
    
    return await asyncio.gather(*[bounded_task(t, tid) for t, tid in tasks])

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Async Agent - Demo")
    print("=" * 60)
    
    tasks = [
        ("Summarize: The benefits of exercise", "task_1"),
        ("Summarize: The importance of sleep", "task_2"),
        ("Summarize: The value of reading", "task_3"),
    ]
    
    concurrency = config.get("concurrency", 3)
    print(f"\n⚡ Processing {len(tasks)} tasks with concurrency={concurrency}")
    
    import time
    start = time.time()
    results = asyncio.run(run_batch(agent, tasks, concurrency))
    total_time = time.time() - start
    
    print(f"\n📊 Results:")
    for r in results:
        print(f"  {r['task_id']}: {r['result'][:60]}... ({r['duration_ms']}ms)")
    print(f"\n⏱️ Total time: {total_time:.2f}s")
    print(f"✅ All {len(results)} tasks completed")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", "-c", type=int, default=DEFAULT_CONFIG["concurrency"])
    args = parser.parse_args()
    run_demo(get_agent(config={"concurrency": args.concurrency}), {"concurrency": args.concurrency})

if __name__ == "__main__": main()
