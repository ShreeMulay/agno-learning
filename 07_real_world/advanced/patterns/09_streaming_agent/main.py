"""
Example #229: Streaming Agent
Category: advanced/patterns
DESCRIPTION: Agent that streams responses for real-time output
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"stream_mode": "token"}

class StreamingResult(BaseModel):
    content: str = Field(description="Full streamed content")
    tokens_generated: int = Field(description="Approximate token count")
    stream_duration: str = Field(description="How long streaming took")
    chunks_sent: int = Field(description="Number of chunks streamed")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Streaming Agent",
        instructions=[
            f"You generate responses suitable for {cfg['stream_mode']} streaming.",
            "Write in a clear, flowing style.",
            "Structure content for progressive delivery.",
            "Maintain coherence across streamed chunks.",
        ],
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Streaming Agent - Demo")
    print("=" * 60)
    
    prompt = "Write a short story about a robot learning to dream"
    print(f"\n📝 Prompt: {prompt}")
    print("\n🌊 Streaming response:\n")
    
    # Simulate streaming with run_stream
    full_content = ""
    chunk_count = 0
    
    try:
        for chunk in agent.run_stream(prompt):
            if hasattr(chunk, 'content') and chunk.content:
                print(chunk.content, end="", flush=True)
                full_content += str(chunk.content)
                chunk_count += 1
    except Exception:
        # Fallback to non-streaming for demo
        response = agent.run(prompt)
        full_content = str(response.content)
        print(full_content[:500])
        chunk_count = 1
    
    print(f"\n\n📊 Stats: ~{len(full_content.split())} words in {chunk_count} chunks")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream-mode", "-s", default=DEFAULT_CONFIG["stream_mode"])
    args = parser.parse_args()
    run_demo(get_agent(config={"stream_mode": args.stream_mode}), {"stream_mode": args.stream_mode})

if __name__ == "__main__": main()
