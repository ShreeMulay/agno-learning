"""
Example #223: Memory Agent
Category: advanced/patterns
DESCRIPTION: Agent with persistent memory across conversation turns
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"memory_type": "conversation"}

class MemoryEntry(BaseModel):
    turn: int = Field(description="Conversation turn number")
    user_input: str = Field(description="What user said")
    agent_response: str = Field(description="Agent's response")
    key_facts: list[str] = Field(description="Facts to remember")

class MemoryResponse(BaseModel):
    response: str = Field(description="Response to current query")
    remembered_context: list[str] = Field(description="Relevant memories used")
    new_facts_stored: list[str] = Field(description="New facts added to memory")
    memory_summary: str = Field(description="Current memory state summary")

class ConversationMemory:
    """Simple in-memory conversation store."""
    def __init__(self):
        self.memories: list[dict] = []
        self.facts: list[str] = []
    
    def add(self, user_input: str, response: str, facts: list[str]):
        self.memories.append({"user": user_input, "agent": response})
        self.facts.extend(facts)
    
    def get_context(self) -> str:
        recent = self.memories[-5:] if len(self.memories) > 5 else self.memories
        context = "\n".join([f"User: {m['user']}\nAgent: {m['agent']}" for m in recent])
        facts = "\n".join([f"- {f}" for f in self.facts[-10:]])
        return f"Recent conversation:\n{context}\n\nKnown facts:\n{facts}"

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

# Global memory instance for demo
_memory = ConversationMemory()

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Memory Agent",
        instructions=[
            f"You maintain {cfg['memory_type']} memory across turns.",
            "Remember user preferences and facts they share.",
            "Reference previous context when relevant.",
            "Update your knowledge as you learn new information.",
        ],
        output_schema=MemoryResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Memory Agent - Demo")
    print("=" * 60)
    
    conversations = [
        "Hi, my name is Alex and I'm a software engineer.",
        "I prefer Python over JavaScript for backend work.",
        "What's my name and what language do I prefer?"
    ]
    
    for i, user_input in enumerate(conversations, 1):
        print(f"\n👤 Turn {i}: {user_input}")
        
        context = _memory.get_context()
        prompt = f"Previous context:\n{context}\n\nCurrent message: {user_input}"
        
        response = agent.run(prompt)
        
        if isinstance(response.content, MemoryResponse):
            r = response.content
            print(f"🤖 Agent: {r.response}")
            if r.new_facts_stored:
                print(f"💾 Stored: {', '.join(r.new_facts_stored)}")
            _memory.add(user_input, r.response, r.new_facts_stored)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-type", "-m", default=DEFAULT_CONFIG["memory_type"])
    args = parser.parse_args()
    run_demo(get_agent(config={"memory_type": args.memory_type}), {"memory_type": args.memory_type})

if __name__ == "__main__": main()
