# Lesson 04: Monitoring and Logging

Configure custom logging, telemetry, and observability for production.

## Key Concepts

### Custom Logging

Agno uses Python's standard logging. You can configure custom loggers:

```python
import logging
from agno.utils.log import configure_agno_logging

# Create custom logger
logger = logging.getLogger("my_agent")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(name)s] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Configure Agno to use it
configure_agno_logging(custom_default_logger=logger)
```

### Named Loggers

Agno recognizes specific logger names:

| Logger Name | Used For |
|-------------|----------|
| `agno` | Agent logs |
| `agno-team` | Team logs |
| `agno-workflow` | Workflow logs |

```python
# Set up named loggers
agent_logger = logging.getLogger("agno")
team_logger = logging.getLogger("agno-team")
```

### File Logging

```python
handler = logging.FileHandler("logs/agent.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Telemetry Control

```python
# Disable telemetry for an agent
agent = Agent(
    model=model,
    telemetry=False  # No anonymous usage data
)

# Or via environment variable
# export AGNO_TELEMETRY=false
```

## Run the Example

```bash
python main.py

# Check the log file
cat tmp/agent.log
```

## Key Points

1. **Standard Logging**: Uses Python's logging module
2. **Named Loggers**: Separate loggers for agents, teams, workflows
3. **Telemetry**: Can be disabled per-instance or globally
4. **Observability**: Integrate with OpenTelemetry, Datadog, etc.

## Exercises

1. Configure logging to write to both console and file
2. Set different log levels for different components
3. Add request/response logging middleware
4. Integrate with an observability platform
