import os
import sys
import json
import importlib.util
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import traceback
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import tiktoken

# Add project root to path for shared imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from shared.model_config import PROVIDER_CONFIGS, check_api_key

# Initialize tokenizer for estimation fallback
tokenizer = tiktoken.get_encoding("cl100k_base")

app = FastAPI(title="Agno Learning Master GUI")

# CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Catalog and Pricing data
CATALOG_PATH = Path(__file__).parent / "data" / "agent_catalog.json"
PRICING_PATH = Path(__file__).parent / "data" / "pricing.json"

with open(CATALOG_PATH, "r") as f:
    AGENT_CATALOG = json.load(f)

with open(PRICING_PATH, "r") as f:
    PRICING_DATA = json.load(f)

# In-memory model cache
MODEL_CACHE = {}

class AgentRunRequest(BaseModel):
    agent_id: str
    provider: str
    model: str
    temperature: float = 0.7
    params: Dict[str, Any] = {}

@app.get("/catalog")
async def get_catalog():
    return AGENT_CATALOG

@app.get("/providers")
async def get_providers():
    """List available providers and their status."""
    providers = []
    for name in PROVIDER_CONFIGS:
        is_active, env_var = check_api_key(name)
        providers.append({
            "id": name,
            "name": name.capitalize(),
            "description": PROVIDER_CONFIGS[name]["description"],
            "is_active": is_active,
            "env_var": env_var,
            "default_model": PROVIDER_CONFIGS[name]["default_model"]
        })
    return providers

async def fetch_models_for_provider(provider: str):
    """Fetch models from provider APIs."""
    if provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key: return []
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("https://openrouter.ai/api/v1/models", 
                                      headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
                return [m["id"] for m in resp.json().get("data", [])]
            except Exception as e:
                logger.warning(f"Failed to fetch OpenRouter models: {e}")
                return []
            
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: return ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("https://api.openai.com/v1/models", 
                                      headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
                data = resp.json()
                return sorted([m["id"] for m in data.get("data", []) if any(x in m["id"].lower() for x in ["gpt", "o1", "o3"])])
            except Exception as e:
                logger.warning(f"Failed to fetch OpenAI models: {e}")
                return ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]

    elif provider == "google":
        api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key: return ["gemini-2.5-flash", "gemini-2.0-flash"]
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"https://generativelanguage.googleapis.com/v1/models?key={api_key}", timeout=10)
                return [m["name"].replace("models/", "") for m in resp.json().get("models", []) if "gemini" in m["name"].lower()]
            except Exception as e:
                logger.warning(f"Failed to fetch Google models: {e}")
                return ["gemini-2.5-flash", "gemini-2.0-flash"]

    elif provider == "cerebras":
        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key: return ["zai-glm-4.6", "llama-3.3-70b"]
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("https://api.cerebras.ai/v1/models", 
                                      headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
                data = resp.json()
                models = data.get("data", data.get("models", []))
                return [m["id"] if isinstance(m, dict) else m for m in models]
            except Exception as e:
                logger.warning(f"Failed to fetch Cerebras models: {e}")
                return ["zai-glm-4.6", "llama-3.3-70b"]
            
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key: return ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("https://api.groq.com/openai/v1/models", 
                                      headers={"Authorization": f"Bearer {api_key}"}, timeout=10)
                return [m["id"] for m in resp.json().get("data", [])]
            except Exception as e:
                logger.warning(f"Failed to fetch Groq models: {e}")
                return ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

    elif provider == "anthropic":
        return ["claude-sonnet-4-5", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
        
    elif provider == "ollama":
        async with httpx.AsyncClient() as client:
            try:
                host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
                resp = await client.get(f"{host}/api/tags", timeout=5)
                return [m["name"] for m in resp.json().get("models", [])]
            except Exception as e:
                logger.warning(f"Failed to fetch Ollama models: {e}")
                return ["llama3.2", "mistral"]
    
    elif provider == "huggingface":
        # HuggingFace has thousands of models - return curated list of popular ones
        # Full search would require HF API with pagination
        api_key = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
        popular_models = [
            "meta-llama/Llama-3.3-70B-Instruct",
            "meta-llama/Llama-3.2-90B-Vision-Instruct",
            "meta-llama/Llama-3.1-405B-Instruct",
            "mistralai/Mixtral-8x22B-Instruct-v0.1",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "google/gemma-2-27b-it",
            "Qwen/Qwen2.5-72B-Instruct",
            "microsoft/Phi-3-medium-128k-instruct",
            "deepseek-ai/DeepSeek-V3",
            "NousResearch/Hermes-3-Llama-3.1-70B",
        ]
        if not api_key:
            return popular_models
        # Could add API search here in future for user-typed queries
        return popular_models
            
    return []

@app.get("/models/reload")
async def reload_all_models():
    """Force refresh of all model lists."""
    MODEL_CACHE.clear()
    return {"status": "Cache cleared"}

@app.get("/models/{provider}")
async def get_models(provider: str, reload: bool = False):
    """Get model list for a provider, with caching."""
    if not reload and provider in MODEL_CACHE:
        return MODEL_CACHE[provider]
    
    models = await fetch_models_for_provider(provider)
    if models:
        MODEL_CACHE[provider] = models
    return models

@app.get("/agent/{agent_id}/source")
async def get_agent_source(agent_id: str):
    """Retrieve the original source code for an agent."""
    agent_info = next((a for a in AGENT_CATALOG if a["id"] == agent_id), None)
    if not agent_info:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    path = PROJECT_ROOT / agent_info["path"]
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Source file not found at {agent_info['path']}")
        
    with open(path, "r") as f:
        return {"content": f.read()}

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
                
                # Hybrid Metrics Implementation
                tokens_estimated = False
                if ot == 0 and full_content:
                    # Fallback to tiktoken estimation
                    ot = len(tokenizer.encode(full_content))
                    it = len(tokenizer.encode(query))
                    tokens_estimated = True
                
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
                        'cost': cost,
                        'estimated': tokens_estimated
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
