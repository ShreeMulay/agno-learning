"""
Example #232: Context Management Agent
Category: advanced/patterns
DESCRIPTION: Agent that manages context window efficiently for long conversations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"max_context_tokens": 4000}

class ContextSummary(BaseModel):
    key_points: list[str] = Field(description="Essential information to retain")
    dropped_details: list[str] = Field(description="Less important details removed")
    context_health: str = Field(description="Context status: healthy, compressed, critical")

class ContextManagedResponse(BaseModel):
    response: str = Field(description="Response to current query")
    context_used: int = Field(description="Approximate tokens of context used")
    context_summary: ContextSummary = Field(description="Context management status")
    compression_applied: bool = Field(description="Whether compression was needed")

class ContextManager:
    """Manages conversation context within token limits."""
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages: list[dict] = []
        self.summary: str = ""
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._compress_if_needed()
    
    def _estimate_tokens(self) -> int:
        return sum(len(m["content"].split()) * 1.3 for m in self.messages)
    
    def _compress_if_needed(self):
        while self._estimate_tokens() > self.max_tokens and len(self.messages) > 2:
            old = self.messages.pop(0)
            self.summary += f" {old['content'][:50]}..."
    
    def get_context(self) -> str:
        context = f"Summary of earlier conversation: {self.summary}\n\n" if self.summary else ""
        context += "\n".join([f"{m['role']}: {m['content']}" for m in self.messages[-5:]])
        return context

_context_mgr = ContextManager()

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Context Management Agent",
        instructions=[
            f"You manage context within {cfg['max_context_tokens']} token limit.",
            "Prioritize recent and important information.",
            "Summarize older context when needed.",
            "Maintain conversation coherence despite compression.",
        ],
        output_schema=ContextManagedResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Context Management Agent - Demo")
    print("=" * 60)
    
    # Simulate a long conversation
    messages = [
        "My name is Sam and I work as a data scientist.",
        "I'm interested in machine learning, especially NLP.",
        "Can you recommend resources for learning transformers?",
        "What's my name and what topic am I interested in?"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"\n👤 Turn {i}: {msg}")
        _context_mgr.add("user", msg)
        
        context = _context_mgr.get_context()
        response = agent.run(f"Context:\n{context}\n\nCurrent: {msg}")
        
        if isinstance(response.content, ContextManagedResponse):
            r = response.content
            print(f"🤖 Agent: {r.response[:150]}...")
            if r.compression_applied:
                print(f"   📦 Context compressed ({r.context_summary.context_health})")
            _context_mgr.add("agent", r.response)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-context-tokens", "-m", type=int, default=DEFAULT_CONFIG["max_context_tokens"])
    args = parser.parse_args()
    run_demo(get_agent(config={"max_context_tokens": args.max_context_tokens}), {"max_context_tokens": args.max_context_tokens})

if __name__ == "__main__": main()
