# MEGA Examples - Reusable Patterns

This document defines the agent patterns used across all 235 examples. Each pattern is a proven combination of Agno features that solves a class of problems.

## Core Patterns

### 1. Tools + Structured Output

**Use Case**: Agents that need to call external APIs and return well-formatted data.

**When to Use**:
- Fetching data from APIs (weather, stocks, search)
- Converting unstructured input to structured response
- Data enrichment workflows

**Example Structure**:
```python
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel

class SearchResult(BaseModel):
    query: str
    results: list[dict]
    summary: str

def get_agent(model=None, config=None):
    return Agent(
        model=model or default_model(),
        tools=[DuckDuckGoTools()],
        response_model=SearchResult,
        instructions=["Search and summarize results"]
    )
```

**Examples Using This Pattern**:
- Lead Qualifier (01)
- CRM Data Enricher (03)
- Hashtag Researcher (20)

---

### 2. Knowledge + Memory

**Use Case**: Agents that need domain expertise and remember context across conversations.

**When to Use**:
- Q&A systems with document knowledge
- Personal assistants that learn preferences
- Multi-turn research workflows

**Example Structure**:
```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.memory.v2.db.sqlite import SqliteDb

def get_agent(model=None, config=None):
    knowledge = PDFKnowledgeBase(path="./docs")
    
    return Agent(
        model=model or default_model(),
        knowledge=knowledge,
        storage=SqliteDb(table_name="agent_sessions", db_file="data.db"),
        session_id=config.get("session_id", "default"),
        instructions=["Answer questions using the knowledge base"]
    )
```

**Examples Using This Pattern**:
- Knowledge Base Search (22)
- Policy Q&A Bot (47)
- Legal Research Assistant (57)

---

### 3. Workflows + Tools

**Use Case**: Multi-step processes that need external data at each step.

**When to Use**:
- ETL pipelines
- Report generation with data fetching
- Approval workflows with notifications

**Example Structure**:
```python
from agno.agent import Agent
from agno.workflow import Workflow

class DataPipeline(Workflow):
    extract_agent: Agent
    transform_agent: Agent
    load_agent: Agent
    
    def run(self, source: str):
        raw = self.extract_agent.run(f"Fetch data from {source}")
        transformed = self.transform_agent.run(f"Clean: {raw.content}")
        result = self.load_agent.run(f"Store: {transformed.content}")
        return result
```

**Examples Using This Pattern**:
- Sales Call Summarizer (07)
- Financial Report Generator (34)
- Invoice Processor (31)

---

### 4. Teams + Structured Output

**Use Case**: Multiple specialized agents collaborating with typed handoffs.

**When to Use**:
- Complex problems needing different expertise
- Quality assurance (writer + reviewer)
- Multi-domain analysis

**Example Structure**:
```python
from agno.agent import Agent
from agno.team import Team

researcher = Agent(name="Researcher", role="Find information")
analyst = Agent(name="Analyst", role="Analyze findings")
writer = Agent(name="Writer", role="Create report")

def get_team(model=None, config=None):
    return Team(
        agents=[researcher, analyst, writer],
        mode="coordinate",  # or "route", "collaborate"
        response_model=FinalReport
    )
```

**Examples Using This Pattern**:
- Social Media Manager (11)
- Ticket Router (21)
- Content Calendar Planner (17)

---

### 5. Memory + Workflows

**Use Case**: Stateful multi-step processes that need history.

**When to Use**:
- Onboarding sequences
- Learning paths with progress
- Long-running projects

**Example Structure**:
```python
from agno.workflow import Workflow
from agno.memory.v2.db.sqlite import SqliteDb

class OnboardingWorkflow(Workflow):
    def __init__(self, user_id: str):
        self.storage = SqliteDb(table_name="onboarding")
        self.session_id = user_id
        
    def run(self, step: str):
        # Load state
        history = self.storage.get_sessions(self.session_id)
        # Process step
        # Save state
```

**Examples Using This Pattern**:
- Onboarding Checklist Tracker (25)
- Compliance Training Tracker (60)
- Study Plan Generator (Education)

---

### 6. Knowledge + Structured Output

**Use Case**: Extract structured data from documents.

**When to Use**:
- Document parsing and classification
- Form data extraction
- Contract analysis

**Example Structure**:
```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from pydantic import BaseModel

class ExtractedData(BaseModel):
    entities: list[str]
    dates: list[str]
    amounts: list[float]
    summary: str

def get_agent(model=None, config=None):
    return Agent(
        model=model or default_model(),
        knowledge=PDFKnowledgeBase(path=config.get("docs_path")),
        response_model=ExtractedData
    )
```

**Examples Using This Pattern**:
- Contract Reviewer (51)
- Resume Screener (41)
- Invoice Processor (31)

---

## Pattern Combinations

Many examples combine multiple patterns:

| Combination | Examples |
|-------------|----------|
| Knowledge + Memory + Tools | Personal Knowledge Base, Research Assistant |
| Teams + Workflows + Memory | Customer Success Suite, HR Automation |
| Tools + Structured Output + Memory | CRM Assistant, Sales Automation |

## Pattern Selection Guide

```
Need external data?
├─ Yes → Add Tools
└─ No → Skip Tools

Need domain expertise?
├─ Yes → Add Knowledge
└─ No → Skip Knowledge

Need conversation history?
├─ Yes → Add Memory
└─ No → Skip Memory

Need typed responses?
├─ Yes → Add Structured Output
└─ No → Use raw responses

Multiple agents needed?
├─ Yes → Use Teams
│   ├─ Sequential handoff? → Coordinate mode
│   ├─ Classification? → Route mode
│   └─ Parallel work? → Collaborate mode
└─ No → Single Agent

Multi-step process?
├─ Yes → Use Workflows
│   ├─ Fixed sequence? → Sequential Workflow
│   └─ Conditional? → Branching Workflow
└─ No → Single run
```

## Anti-Patterns to Avoid

### 1. Over-Engineering
❌ Using Teams when a single Agent suffices
✅ Start simple, add complexity when needed

### 2. Missing Error Handling
❌ Assuming tools always succeed
✅ Always wrap tool calls with fallback handling

### 3. Hardcoded State
❌ Using global variables for state
✅ Use Memory with proper session IDs

### 4. Blocking on Optional Data
❌ Failing when optional API is down
✅ Graceful degradation with cached/default data

### 5. Unbounded Context
❌ Loading entire document into prompt
✅ Use Knowledge with vector search for relevance
