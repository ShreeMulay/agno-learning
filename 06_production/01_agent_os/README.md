# Lesson 01: AgentOS Runtime

Deploy agents as production-ready FastAPI applications using AgentOS.

## What is AgentOS?

AgentOS is Agno's production-ready runtime that:
- Runs entirely within your own infrastructure
- Provides a FastAPI backend out of the box
- Offers a web interface for managing agents
- Handles session persistence, knowledge, and more

## Key Concepts

### AgentOS Structure

```python
from agno.os import AgentOS
from agno.agent import Agent

agent_os = AgentOS(
    id="my-os",                    # Unique identifier
    description="My Agent System", # Human-readable description
    agents=[agent1, agent2],       # Agents to expose
    teams=[team1],                 # Optional: Teams
    workflows=[workflow1],         # Optional: Workflows
)
```

### Getting the FastAPI App

```python
# AgentOS wraps everything in a FastAPI app
app = agent_os.get_app()

# Run with built-in server
agent_os.serve(app="my_os:app", reload=True)

# Or use uvicorn directly
# uvicorn my_os:app --reload --port 7777
```

### Auto-Generated Endpoints

AgentOS automatically creates these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root info |
| `/config` | GET | AgentOS configuration |
| `/docs` | GET | OpenAPI documentation |
| `/agents` | GET | List all agents |
| `/agents/{id}/run` | POST | Run an agent |
| `/sessions` | GET | List sessions |

## Run the Example

```bash
# Start the AgentOS server
python main.py

# Then visit:
# - http://localhost:7777/docs - API documentation
# - http://localhost:7777/config - Configuration
```

## Key Points

1. **Production-Ready**: Built on FastAPI with async support
2. **Self-Contained**: Run locally or in your cloud
3. **Extensible**: Add custom routes, middleware, databases
4. **Observable**: Built-in config and health endpoints

## Exercises

1. Add a second agent to the AgentOS
2. Access the `/docs` endpoint and test the API
3. Make a POST request to `/agents/{id}/run`
4. Explore the `/config` endpoint output
