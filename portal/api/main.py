from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import asyncio
from typing import Optional

from .registry import registry, PROJECT_ROOT

app = FastAPI(title="Agno Learning Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/modules")
async def list_modules():
    return registry.modules

@app.get("/api/v1/lessons/{module}/{lesson}")
async def get_lesson(module: str, lesson: str):
    key = f"{module}/{lesson}"
    if key not in registry.lessons:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson_data = registry.lessons[key]
    readme_path = PROJECT_ROOT / module / lesson / "README.md"
    
    content = ""
    if readme_path.exists():
        content = readme_path.read_text()
        
    return {
        **lesson_data,
        "readme": content
    }

@app.get("/api/v1/lessons/{module}/{lesson}/code")
async def get_lesson_code(module: str, lesson: str):
    code_path = PROJECT_ROOT / module / lesson / "main.py"
    if not code_path.exists():
        raise HTTPException(status_code=404, detail="Source code not found")
    
    return {"code": code_path.read_text()}

@app.websocket("/ws/api/v1/agents/{module}/{lesson}/run")
async def run_agent_ws(websocket: WebSocket, module: str, lesson: str):
    await websocket.accept()
    
    try:
        # Initial config from client
        data = await websocket.receive_text()
        config = json.loads(data)
        
        provider = config.get("provider")
        model = config.get("model")
        temperature = config.get("temperature")
        max_tokens = config.get("max_tokens")
        message = config.get("message")
        
        if not message:
            await websocket.send_json({"error": "Message is required"})
            await websocket.close()
            return

        # Instantiate agent
        agent = registry.get_agent_instance(
            module, 
            lesson, 
            provider=provider, 
            model=model, 
            temperature=temperature
        )
        
        # Apply max_tokens if provided
        if max_tokens and hasattr(agent, 'model') and agent.model:
            agent.model.max_tokens = int(max_tokens)
        
        # Stream response
        await websocket.send_json({"type": "status", "content": "Agent started..."})
        
        # Capture streaming response
        # Agno agents usually have .run(stream=True) or similar
        # For simplicity in this implementation, we'll use a generic loop
        
        response_generator = agent.run(message, stream=True)
        
        for chunk in response_generator:
            if hasattr(chunk, 'content'):
                content = chunk.content
            else:
                content = str(chunk)
                
            if content:
                await websocket.send_json({"type": "content", "content": content})
        
        await websocket.send_json({"type": "done"})
        
    except WebSocketDisconnect:
        print(f"Client disconnected from {module}/{lesson}")
    except Exception as e:
        print(f"Error running agent: {e}")
        await websocket.send_json({"type": "error", "content": str(e)})
    finally:
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
