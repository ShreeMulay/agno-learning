"""
Example #121: Enrollment Processor
Category: education/admin
DESCRIPTION: Processes student enrollments and registrations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"enrollment_type": "new_student"}

class EnrollmentResult(BaseModel):
    student_name: str = Field(description="Student name")
    enrollment_status: str = Field(description="approved, pending, denied")
    student_id: str = Field(description="Assigned student ID")
    grade_level: str = Field(description="Grade placement")
    courses: list[str] = Field(description="Enrolled courses")
    missing_documents: list[str] = Field(description="Documents needed")
    next_steps: list[str] = Field(description="Next steps for completion")
    notifications: list[str] = Field(description="Notifications to send")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Enrollment Processor",
        instructions=["Process student enrollments", "Verify required documents", "Assign appropriate grade level and courses", "Generate required notifications"],
        output_schema=EnrollmentResult, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Enrollment Processor - Demo\n" + "=" * 60)
    response = agent.run(f"Process {config['enrollment_type']} enrollment: Student John Doe, transferring from Lincoln Middle School, Grade 7, has transcripts and immunization records")
    result = response.content
    if isinstance(result, EnrollmentResult):
        print(f"\nStudent: {result.student_name} | ID: {result.student_id}")
        print(f"Status: {result.enrollment_status} | Grade: {result.grade_level}")
        print(f"Courses: {', '.join(result.courses[:3])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--enrollment-type", "-t", default=DEFAULT_CONFIG["enrollment_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"enrollment_type": args.enrollment_type})

if __name__ == "__main__": main()
