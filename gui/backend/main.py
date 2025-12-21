import os
import sys
import json
import importlib.util
import asyncio
import time
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Add project root to path for shared imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="Agno Learning Master GUI")

# CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Catalog
CATALOG_PATH = Path(__file__).parent / "data" / "agent_catalog.json"
PRICING_PATH = Path(__file__).parent / "data" / "pricing.json"

with open(CATALOG_PATH, "r") as f:
    AGENT_CATALOG = json.load(f)

with open(PRICING_PATH, "r") as f:
    PRICING_DATA = json.load(f)

class AgentRunRequest(BaseModel):
    agent_id: str
    provider: str
    model: str
    temperature: float = 0.7
    params: Dict[str, Any] = {}

@app.get("/catalog")
async def get_catalog():
    return AGENT_CATALOG

@app.get("/models/openrouter")
async def get_openrouter_models():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"data": []}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            return {"data": [], "error": str(e)}

def load_agent(path: Path):
    """Load an agent module from a Path object."""
    abs_path = path if path.is_absolute() else PROJECT_ROOT / path
    module_name = f"dynamic_{abs_path.stem}_{abs_path.parent.name}"
    
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load module at {abs_path}")
        
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

@app.post("/run")
async def run_agent(request: AgentRunRequest):
    agent_info = next((a for a in AGENT_CATALOG if a["id"] == request.agent_id), None)
    if not agent_info:
        raise HTTPException(status_code=404, detail="Agent not found")

    async def event_generator():
        try:
            from shared.model_config import get_model
            model = get_model(
                provider=request.provider,
                model=request.model,
                temperature=request.temperature
            )

            agent_dir = PROJECT_ROOT / agent_info["dir"]
            agent_path = PROJECT_ROOT / agent_info["path"]
            old_cwd = os.getcwd()
            os.chdir(agent_dir)
            
            try:
                # Load agent using full path from catalog
                module = load_agent(agent_path)
                
                # Setup params for agent.run()
                # Most agents take positional query + optional kwargs
                call_args = {}
                
                # Map catalog params to call_args
                query = "Hello!"
                for p in agent_info["params"]:
                    val = request.params.get(p["name"]) or p.get("default", "")
                    if p.get("is_positional"):
                        query = val
                    else:
                        # Only add if it has a value
                        if val:
                            call_args[p["name"]] = val

                agent = module.get_agent(model=model)

                start_time = time.time()
                
                # Streaming implementation
                # Combine positional query with named parameters
                stream = agent.run(query, stream=True, **call_args)
                full_content = ""
                it, ot = 0, 0
                
                for chunk in stream:
                    if hasattr(chunk, "content") and chunk.content:
                        full_content += chunk.content
                        yield f"data: {json.dumps({'event': 'chunk', 'content': chunk.content})}\n\n"
                    
                    m = getattr(chunk, "metrics", None)
                    if m:
                        # Extract it/ot correctly from metrics object
                        it = max(it, getattr(m, "input_tokens", 0) or 0)
                        ot = max(ot, getattr(m, "output_tokens", 0) or 0)

                end_time = time.time()
                duration = end_time - start_time
                
                # Final calculation
                rate = PRICING_DATA.get(request.provider, {}).get(request.model, {"input": 0, "output": 0})
                cost = (it * rate["input"] + ot * rate["output"]) / 1_000_000
                
                yield f"data: {json.dumps({
                    'event': 'complete',
                    'content': full_content,
                    'metrics': {
                        'duration': duration,
                        'input_tokens': it,
                        'output_tokens': ot,
                        'tps': ot / duration if duration > 0 else 0,
                        'cost': cost
                    }
                })}\n\n"
                
            finally:
                os.chdir(old_cwd)

        except Exception as e:
            err_msg = f"{str(e)}\n{traceback.format_exc()}"
            yield f"data: {json.dumps({'event': 'error', 'message': err_msg})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
