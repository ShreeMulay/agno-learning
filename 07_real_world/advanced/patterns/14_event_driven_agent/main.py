"""
Example #234: Event-Driven Agent
Category: advanced/patterns
DESCRIPTION: Agent that responds to events and triggers appropriate actions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field
from datetime import datetime

DEFAULT_CONFIG = {"event_types": ["user_action", "system", "scheduled"]}

class Event(BaseModel):
    event_type: str = Field(description="Type of event")
    source: str = Field(description="Event source")
    payload: dict = Field(description="Event data")
    timestamp: str = Field(description="When event occurred")

class EventAction(BaseModel):
    action_type: str = Field(description="Action to take")
    target: str = Field(description="Action target")
    parameters: dict = Field(description="Action parameters")
    priority: str = Field(description="high, medium, low")

class EventResponse(BaseModel):
    event_received: Event = Field(description="The triggering event")
    event_classification: str = Field(description="How event was classified")
    actions_triggered: list[EventAction] = Field(description="Actions to execute")
    notifications: list[str] = Field(description="Notifications to send")
    follow_up_events: list[str] = Field(description="Events that may follow")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Event-Driven Agent",
        instructions=[
            f"You handle events of types: {cfg['event_types']}.",
            "Classify incoming events appropriately.",
            "Trigger relevant actions based on event type.",
            "Predict potential follow-up events.",
        ],
        output_schema=EventResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Event-Driven Agent - Demo")
    print("=" * 60)
    
    # Simulate events
    events = [
        {"type": "user_action", "source": "web_app", "payload": {"action": "purchase", "amount": 99.99}},
        {"type": "system", "source": "monitoring", "payload": {"alert": "high_cpu", "level": 85}},
        {"type": "scheduled", "source": "cron", "payload": {"job": "daily_report", "time": "09:00"}},
    ]
    
    for event_data in events:
        event = Event(
            event_type=event_data["type"],
            source=event_data["source"],
            payload=event_data["payload"],
            timestamp=datetime.now().isoformat()
        )
        
        print(f"\n⚡ Event: {event.event_type} from {event.source}")
        print(f"   Payload: {event.payload}")
        
        response = agent.run(f"Process this event: {event.model_dump_json()}")
        
        if isinstance(response.content, EventResponse):
            r = response.content
            print(f"📋 Classification: {r.event_classification}")
            print(f"🎯 Actions Triggered:")
            for action in r.actions_triggered:
                print(f"   [{action.priority}] {action.action_type} → {action.target}")
            if r.notifications:
                print(f"🔔 Notifications: {', '.join(r.notifications)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-types", "-e", nargs="+", default=DEFAULT_CONFIG["event_types"])
    args = parser.parse_args()
    run_demo(get_agent(config={"event_types": args.event_types}), {"event_types": args.event_types})

if __name__ == "__main__": main()
