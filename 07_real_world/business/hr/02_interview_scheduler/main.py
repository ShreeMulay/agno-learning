"""
Example #042: Interview Scheduler
Category: business/hr

DESCRIPTION:
Matches interviewer and candidate availability to schedule interviews.
Handles time zones, generates calendar invites, and sends reminders.

PATTERNS:
- Reasoning (scheduling logic)
- Structured Output (ScheduleResult)

ARGUMENTS:
- candidate_availability (str): Candidate's available slots
- interviewer_availability (str): Interviewer's available slots
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "candidate_availability": """
    Candidate: Sarah Chen
    Timezone: PST (UTC-8)
    Available:
    - Monday Dec 16: 9am-12pm, 2pm-5pm
    - Tuesday Dec 17: 10am-4pm
    - Wednesday Dec 18: 9am-11am, 1pm-3pm
    - Thursday Dec 19: All day (9am-5pm)
    """,
    "interviewer_availability": """
    Interviewer 1: John Smith (Hiring Manager)
    Timezone: EST (UTC-5)
    Available: Mon 2pm-5pm, Tue 9am-12pm, Thu 10am-2pm
    
    Interviewer 2: Lisa Wang (Tech Lead)
    Timezone: PST (UTC-8)
    Available: Mon 10am-12pm, Wed 1pm-5pm, Thu 9am-12pm
    
    Interviewer 3: Mike Johnson (HR)
    Timezone: CST (UTC-6)
    Available: Tue 1pm-4pm, Wed 9am-11am, Thu 2pm-5pm
    """,
    "interview_duration": 60,
}


class InterviewSlot(BaseModel):
    interviewer: str = Field(description="Interviewer name")
    role: str = Field(description="Interviewer's role")
    date: str = Field(description="Interview date")
    start_time: str = Field(description="Start time in candidate's timezone")
    end_time: str = Field(description="End time in candidate's timezone")
    interviewer_local_time: str = Field(description="Time in interviewer's timezone")


class ScheduleResult(BaseModel):
    candidate_name: str = Field(description="Candidate name")
    candidate_timezone: str = Field(description="Candidate's timezone")
    scheduled_interviews: list[InterviewSlot] = Field(description="Confirmed slots")
    unscheduled_interviewers: list[str] = Field(description="Couldn't find slot")
    scheduling_notes: list[str] = Field(description="Any concerns or conflicts")
    calendar_invite_text: str = Field(description="Draft calendar invite")
    reminder_schedule: list[str] = Field(description="When to send reminders")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    duration = cfg.get("interview_duration", 60)
    
    return Agent(
        model=model or default_model(),
        name="Interview Scheduler",
        instructions=[
            "You are an expert interview coordinator.",
            f"Schedule {duration}-minute interview slots.",
            "",
            "Scheduling Rules:",
            "- Find overlapping availability between candidate and interviewers",
            "- Account for timezone differences accurately",
            "- Allow 15-min buffer between interviews",
            "- Prefer morning slots when possible",
            "- Group interviews on same day if feasible",
            "",
            "Always display times in candidate's timezone with interviewer's local time noted.",
        ],
        output_schema=ScheduleResult,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Interview Scheduler - Demo")
    print("=" * 60)
    
    candidate = config.get("candidate_availability", DEFAULT_CONFIG["candidate_availability"])
    interviewers = config.get("interviewer_availability", DEFAULT_CONFIG["interviewer_availability"])
    
    query = f"""Schedule interviews:

CANDIDATE AVAILABILITY:
{candidate}

INTERVIEWER AVAILABILITY:
{interviewers}"""
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, ScheduleResult):
        print(f"\n👤 Candidate: {result.candidate_name}")
        print(f"🌍 Timezone: {result.candidate_timezone}")
        
        print(f"\n📅 Scheduled Interviews:")
        for slot in result.scheduled_interviews:
            print(f"  • {slot.date} {slot.start_time}-{slot.end_time}")
            print(f"    {slot.interviewer} ({slot.role})")
            print(f"    Their time: {slot.interviewer_local_time}")
        
        if result.unscheduled_interviewers:
            print(f"\n⚠️ Couldn't schedule:")
            for name in result.unscheduled_interviewers:
                print(f"  • {name}")
        
        print(f"\n📧 Calendar Invite:")
        print(f"  {result.calendar_invite_text[:200]}...")
        
        print(f"\n⏰ Reminders:")
        for r in result.reminder_schedule:
            print(f"  • {r}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Interview Scheduler")
    parser.add_argument("--candidate", "-c", type=str, default=DEFAULT_CONFIG["candidate_availability"])
    parser.add_argument("--interviewers", "-i", type=str, default=DEFAULT_CONFIG["interviewer_availability"])
    args = parser.parse_args()
    agent = get_agent(config={"candidate_availability": args.candidate, "interviewer_availability": args.interviewers})
    run_demo(agent, {"candidate_availability": args.candidate, "interviewer_availability": args.interviewers})


if __name__ == "__main__":
    main()
