#!/usr/bin/env python3
"""Lesson 02: FastAPI Integration - Custom routes and middleware.

This example shows how to integrate your own FastAPI routes
and middleware with AgentOS.

Run with:
    python main.py

Then test:
    curl http://localhost:7777/health
    curl http://localhost:7777/api/v1/customers
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from agno.agent import Agent
from agno.os import AgentOS
from agno.db.sqlite import AsyncSqliteDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Create custom FastAPI app
def create_custom_app() -> FastAPI:
    """Create a custom FastAPI app with routes and middleware."""
    
    app = FastAPI(
        title="Agno Learning API",
        description="Custom FastAPI app with AgentOS integration",
        version="1.0.0",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request timing middleware
    @app.middleware("http")
    async def add_timing_header(request: Request, call_next: Callable):
        start = time.time()
        response: Response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for load balancers."""
        return {
            "status": "healthy",
            "timestamp": time.time(),
        }
    
    # Create API router for versioned endpoints
    api_router = APIRouter(prefix="/api/v1", tags=["API v1"])
    
    @api_router.get("/customers")
    async def list_customers():
        """List all customers."""
        return [
            {"id": 1, "name": "Acme Corp", "plan": "enterprise"},
            {"id": 2, "name": "StartupXYZ", "plan": "starter"},
        ]
    
    @api_router.get("/customers/{customer_id}")
    async def get_customer(customer_id: int):
        """Get a specific customer."""
        customers = {
            1: {"id": 1, "name": "Acme Corp", "plan": "enterprise"},
            2: {"id": 2, "name": "StartupXYZ", "plan": "starter"},
        }
        return customers.get(customer_id, {"error": "Not found"})
    
    @api_router.post("/feedback")
    async def submit_feedback(feedback: dict):
        """Submit user feedback."""
        return {
            "status": "received",
            "feedback_id": "fb_123",
            "message": feedback.get("message", ""),
        }
    
    app.include_router(api_router)
    
    return app


def create_agent_os(model, custom_app: FastAPI):
    """Create AgentOS with custom FastAPI app."""
    
    db = AsyncSqliteDb(
        id="fastapi_demo_db",
        db_file="tmp/fastapi_demo.db"
    )
    
    assistant = Agent(
        name="Assistant",
        model=model,
        db=db,
        instructions=["You are a helpful assistant for our API."],
        markdown=True,
    )
    
    # Pass custom app to AgentOS
    agent_os = AgentOS(
        id="fastapi-demo-os",
        description="AgentOS with custom FastAPI integration",
        agents=[assistant],
        base_app=custom_app,  # Your custom FastAPI app
    )
    
    return agent_os


def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        name="Assistant",
        model=model,
        instructions=["You are a helpful assistant for our API."],
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="FastAPI Integration Demo")
    add_model_args(parser)
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()

    print_header("Lesson 02: FastAPI Integration")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    # Create custom FastAPI app
    custom_app = create_custom_app()
    
    print_section("Custom Routes")
    print("  GET  /health         - Health check")
    print("  GET  /api/v1/customers    - List customers")
    print("  GET  /api/v1/customers/{id} - Get customer")
    print("  POST /api/v1/feedback     - Submit feedback")
    
    # Create AgentOS with custom app
    agent_os = create_agent_os(model, custom_app)
    
    print_section("Starting Server")
    print(f"  http://localhost:{args.port}")
    print()
    
    app = agent_os.get_app()
    agent_os.serve(
        app="06_production.02_fastapi_integration.main:app",
        port=args.port,
        reload=True
    )


# Export for uvicorn
def get_app():
    from shared.model_config import get_model
    model = get_model("openrouter")
    custom_app = create_custom_app()
    agent_os = create_agent_os(model, custom_app)
    return agent_os.get_app()

app = None
try:
    app = get_app()
except Exception:
    pass


if __name__ == "__main__":
    main()
