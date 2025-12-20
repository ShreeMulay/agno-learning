# Lesson 02: FastAPI Integration

Add custom routes and middleware to your AgentOS.

## Key Concepts

### Bring Your Own FastAPI App

```python
from fastapi import FastAPI
from agno.os import AgentOS

# Create your custom FastAPI app
app = FastAPI(title="My Custom App")

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Pass to AgentOS
agent_os = AgentOS(
    agents=[my_agent],
    base_app=app  # Your custom app
)

app = agent_os.get_app()
```

### Adding Custom Routers

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/users")
async def list_users():
    return [{"id": 1, "name": "Alice"}]

# Add router to your app before passing to AgentOS
app.include_router(router)
```

### Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Run the Example

```bash
python main.py

# Then test:
# curl http://localhost:7777/health
# curl http://localhost:7777/api/v1/customers
```

## Key Points

1. **base_app**: Pass your FastAPI app to AgentOS
2. **Custom Routes**: Add any route before or after AgentOS
3. **Middleware**: CORS, auth, logging all work
4. **Routers**: Organize routes with FastAPI routers

## Exercises

1. Add a POST endpoint that accepts JSON
2. Add request logging middleware
3. Create a protected route with API key validation
4. Add a custom error handler
