from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from memgraph_core import MemGraphCore
from llm_interface import llm_client
import uuid

from fastapi.middleware.cors import CORSMiddleware

# Initialize App & Core
app = FastAPI(title="MemGraph API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for hackathon demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memgraph = MemGraphCore()

# Data Models
class ChatRequest(BaseModel):
    message: str
    api_key: Optional[str] = None

class MemoryResponse(BaseModel):
    id: str
    tier: str
    content: str
    score: float

class ChatResponse(BaseModel):
    response: str
    active_memories: List[MemoryResponse]
    latency_ms: float
    cache_hit: bool

# State
class GameState:
    chat_history = []
    
state = GameState()

@app.get("/")
def health_check():
    return {"status": "online", "system": "MemGraph Nuclear Core"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    import time
    start_time = time.time()
    
    # Configure LLM if key provided
    if req.api_key:
        llm_client.set_api_key(req.api_key)
    
    # 1. Ingest
    mem = memgraph.add_memory(req.message, role="user")
    
    # 2. Retrieve
    active_memories = memgraph.retrieve(req.message)
    
    # 3. Generate
    response_text = llm_client.generate_memgraph_response(req.message, active_memories)
    
    # 4. Store Response
    memgraph.add_memory(response_text, role="assistant")
    
    # 5. Maintenance (Background simplified for now)
    memgraph.run_pruning_cycle()
    memgraph.consolidate_memories()
    
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    
    # Format Response
    mem_responses = []
    for m in active_memories:
        mem_responses.append(MemoryResponse(
            id=m.internal_code,
            tier=m.tier.value,
            content=m.content,
            score=m.half_life_score
        ))
        
    return ChatResponse(
        response=response_text,
        active_memories=mem_responses,
        latency_ms=latency,
        cache_hit=(memgraph.neural_cache_hits > 0)
    )

@app.get("/stats")
def get_stats():
    return {
        "l1_count": len(memgraph.l1_cache),
        "l2_count": len(memgraph.l2_episodic),
        "l3_count": len(memgraph.l3_semantic),
        "total_turns": memgraph.global_turn
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
