"""
Example #233: State Machine Agent
Category: advanced/patterns
DESCRIPTION: Agent that operates as a finite state machine with defined transitions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field
from enum import Enum

DEFAULT_CONFIG = {"initial_state": "greeting"}

class ConversationState(str, Enum):
    GREETING = "greeting"
    GATHERING_INFO = "gathering_info"
    PROCESSING = "processing"
    CONFIRMING = "confirming"
    COMPLETE = "complete"
    ERROR = "error"

class StateTransition(BaseModel):
    from_state: str = Field(description="Previous state")
    to_state: str = Field(description="New state")
    trigger: str = Field(description="What caused transition")
    valid: bool = Field(description="Whether transition is valid")

class StateMachineResponse(BaseModel):
    current_state: str = Field(description="Current state")
    response: str = Field(description="Response for current state")
    transition: StateTransition = Field(description="State transition info")
    available_actions: list[str] = Field(description="Valid actions in current state")
    progress: int = Field(description="Progress percentage 0-100")

# Valid state transitions
TRANSITIONS = {
    "greeting": ["gathering_info"],
    "gathering_info": ["processing", "gathering_info"],
    "processing": ["confirming", "error"],
    "confirming": ["complete", "gathering_info"],
    "complete": ["greeting"],
    "error": ["gathering_info", "greeting"],
}

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="State Machine Agent",
        instructions=[
            f"You operate as a state machine, starting in {cfg['initial_state']}.",
            "Follow defined state transitions strictly.",
            "Guide users through the workflow.",
            f"Valid transitions: {TRANSITIONS}",
        ],
        output_schema=StateMachineResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  State Machine Agent - Demo")
    print("=" * 60)
    
    current_state = config.get("initial_state", "greeting")
    inputs = ["Hi", "I need to book a flight to NYC", "Yes, that's correct"]
    
    for user_input in inputs:
        print(f"\n👤 User: {user_input}")
        print(f"📍 Current State: {current_state}")
        
        response = agent.run(f"""
        Current state: {current_state}
        Valid transitions from here: {TRANSITIONS.get(current_state, [])}
        User input: {user_input}
        
        Process input and transition if appropriate.""")
        
        if isinstance(response.content, StateMachineResponse):
            r = response.content
            print(f"🤖 Agent: {r.response}")
            print(f"🔄 Transition: {r.transition.from_state} → {r.transition.to_state}")
            print(f"📊 Progress: {r.progress}%")
            current_state = r.current_state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial-state", "-s", default=DEFAULT_CONFIG["initial_state"])
    args = parser.parse_args()
    run_demo(get_agent(config={"initial_state": args.initial_state}), {"initial_state": args.initial_state})

if __name__ == "__main__": main()
