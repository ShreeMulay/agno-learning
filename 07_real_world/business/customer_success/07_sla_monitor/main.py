"""
Example #027: SLA Monitor
Category: business/customer_success

DESCRIPTION:
Tracks SLA compliance in real-time, alerts on breaches, and provides
performance analytics. Monitors response times, resolution times, and
identifies patterns in SLA violations.

PATTERNS:
- Tools (time calculations)
- Workflows (alert triggers)
- Structured Output (SLAReport)

ARGUMENTS:
- tickets (str): Ticket data with timestamps. Default: sample
- sla_config (str): SLA thresholds. Default: sample
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "tickets": """
    Active Tickets:
    
    TKT-101: Enterprise, Priority P1, Created 2h ago, No response yet
    TKT-102: Pro, Priority P2, Created 6h ago, First response 1h ago
    TKT-103: Enterprise, Priority P1, Created 45m ago, First response 30m ago
    TKT-104: Standard, Priority P3, Created 20h ago, First response 18h ago
    TKT-105: Enterprise, Priority P2, Created 4h ago, No response yet
    TKT-106: Pro, Priority P1, Created 90m ago, First response 60m ago
    TKT-107: Standard, Priority P2, Created 12h ago, First response 8h ago
    
    Recent Resolutions (last 24h):
    TKT-098: Enterprise P1, Created to Resolved: 3h (SLA: 4h) ✓
    TKT-099: Pro P2, Created to Resolved: 26h (SLA: 24h) ✗
    TKT-100: Standard P3, Created to Resolved: 70h (SLA: 72h) ✓
    """,
    "sla_config": """
    SLA Targets:
    
    Enterprise:
    - P1: First Response 1h, Resolution 4h
    - P2: First Response 4h, Resolution 24h
    - P3: First Response 8h, Resolution 72h
    
    Pro:
    - P1: First Response 2h, Resolution 8h
    - P2: First Response 8h, Resolution 24h
    - P3: First Response 24h, Resolution 72h
    
    Standard:
    - P1: First Response 4h, Resolution 24h
    - P2: First Response 24h, Resolution 48h
    - P3: First Response 48h, Resolution 72h
    """,
}


# =============================================================================
# Output Schema
# =============================================================================

class TicketSLAStatus(BaseModel):
    """SLA status for individual ticket."""
    
    ticket_id: str = Field(description="Ticket ID")
    tier: str = Field(description="Customer tier")
    priority: str = Field(description="Priority level")
    response_sla: str = Field(description="Response SLA status")
    resolution_sla: str = Field(description="Resolution SLA status")
    time_remaining: str = Field(description="Time until SLA breach")
    status: str = Field(description="met/at_risk/breached")
    action_needed: str = Field(description="Required action")


class SLAMetrics(BaseModel):
    """Overall SLA performance metrics."""
    
    response_sla_rate: float = Field(description="% tickets meeting response SLA")
    resolution_sla_rate: float = Field(description="% tickets meeting resolution SLA")
    avg_response_time: str = Field(description="Average first response time")
    avg_resolution_time: str = Field(description="Average resolution time")
    tickets_at_risk: int = Field(description="Tickets approaching breach")
    tickets_breached: int = Field(description="Tickets currently breached")


class SLAAlert(BaseModel):
    """SLA alert."""
    
    severity: str = Field(description="critical/warning/info")
    ticket_id: str = Field(description="Affected ticket")
    message: str = Field(description="Alert message")
    time_to_breach: str = Field(description="Time until/since breach")
    escalation_needed: bool = Field(description="Needs escalation")


class BreachPattern(BaseModel):
    """Pattern in SLA breaches."""
    
    pattern: str = Field(description="Pattern description")
    frequency: str = Field(description="How often this occurs")
    root_cause: str = Field(description="Likely root cause")
    recommendation: str = Field(description="How to address")


class SLAReport(BaseModel):
    """Complete SLA monitoring report."""
    
    report_time: str = Field(description="Report generation time")
    metrics: SLAMetrics = Field(description="Overall metrics")
    active_tickets: list[TicketSLAStatus] = Field(description="Current ticket status")
    alerts: list[SLAAlert] = Field(description="Active alerts")
    breach_patterns: list[BreachPattern] = Field(description="Identified patterns")
    team_performance: dict = Field(description="Performance by team/agent")
    recommendations: list[str] = Field(description="Improvement suggestions")
    executive_summary: str = Field(description="Summary for leadership")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the SLA Monitor agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for SLA monitoring
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="SLA Monitor",
        instructions=[
            "You are an SLA compliance monitoring specialist.",
            "Track SLA performance and alert on violations.",
            "",
            "SLA Configuration:",
            cfg["sla_config"],
            "",
            "Status Definitions:",
            "- MET: SLA target achieved",
            "- AT_RISK: <30 minutes to breach",
            "- BREACHED: Past SLA target",
            "",
            "Alert Severity:",
            "- CRITICAL: P1 breach or imminent",
            "- WARNING: P2 at risk, or P1 approaching",
            "- INFO: P3 status updates",
            "",
            "Escalation Rules:",
            "- Enterprise P1 breach → Immediate exec notification",
            "- Any breach → Manager notification",
            "- Pattern detected → Process review triggered",
            "",
            "Calculate accurate time differences and flag issues proactively.",
        ],
        output_schema=SLAReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of SLA monitoring."""
    print("\n" + "=" * 60)
    print("  SLA Monitor - Demo")
    print("=" * 60)
    
    tickets = config.get("tickets", DEFAULT_CONFIG["tickets"])
    sla_config = config.get("sla_config", DEFAULT_CONFIG["sla_config"])
    
    query = f"""
    Monitor SLA compliance for these tickets:
    
    {tickets}
    
    SLA Configuration:
    {sla_config}
    
    Generate alerts, identify patterns, and recommend improvements.
    """
    
    print("\nAnalyzing SLA compliance...")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, SLAReport):
        print(f"\n{'='*50}")
        print(f"SLA MONITORING REPORT")
        print(f"Generated: {result.report_time}")
        print(f"{'='*50}")
        
        m = result.metrics
        print(f"\n📊 Performance Metrics:")
        print(f"  Response SLA: {m.response_sla_rate:.1f}%")
        print(f"  Resolution SLA: {m.resolution_sla_rate:.1f}%")
        print(f"  Avg Response: {m.avg_response_time}")
        print(f"  Avg Resolution: {m.avg_resolution_time}")
        print(f"  ⚠️ At Risk: {m.tickets_at_risk} | 🔴 Breached: {m.tickets_breached}")
        
        if result.alerts:
            print(f"\n🚨 ALERTS:")
            for alert in result.alerts:
                icon = "🔴" if alert.severity == "critical" else "🟡" if alert.severity == "warning" else "🔵"
                esc = " [ESCALATE]" if alert.escalation_needed else ""
                print(f"  {icon} {alert.ticket_id}: {alert.message}{esc}")
                print(f"     Time: {alert.time_to_breach}")
        
        print(f"\n📋 Active Tickets:")
        for ticket in result.active_tickets:
            icon = "🟢" if ticket.status == "met" else "🟡" if ticket.status == "at_risk" else "🔴"
            print(f"  {icon} {ticket.ticket_id} ({ticket.tier} {ticket.priority})")
            print(f"     Response: {ticket.response_sla} | Resolution: {ticket.resolution_sla}")
            if ticket.status != "met":
                print(f"     ⏱️ {ticket.time_remaining} | Action: {ticket.action_needed}")
        
        if result.breach_patterns:
            print(f"\n📈 Breach Patterns:")
            for pattern in result.breach_patterns:
                print(f"\n  Pattern: {pattern.pattern}")
                print(f"    Frequency: {pattern.frequency}")
                print(f"    Cause: {pattern.root_cause}")
                print(f"    Fix: {pattern.recommendation}")
        
        print(f"\n💡 Recommendations:")
        for rec in result.recommendations[:4]:
            print(f"  • {rec}")
        
        print(f"\n📋 Executive Summary:")
        print(f"  {result.executive_summary}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SLA Monitor - Track SLA compliance"
    )
    
    parser.add_argument(
        "--tickets", "-t",
        type=str,
        default=DEFAULT_CONFIG["tickets"],
        help="Ticket data"
    )
    
    args = parser.parse_args()
    
    config = {
        "tickets": args.tickets,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
