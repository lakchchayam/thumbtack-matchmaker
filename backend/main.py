from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from database import db
from models import Pro, UserRequest, AgentResponse
from agent import run_agent

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Thumbtack AI Matchmaker API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Setup CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Initialize DB (and Chroma/Embeddings)
    db._initialize_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "db_initialized": db.is_initialized}

@app.get("/pros", response_model=List[Pro])
def get_all_pros():
    return db.get_all_pros()

@app.post("/chat", response_model=AgentResponse)
@limiter.limit("5/minute")
def chat_with_agent(request: Request, user_request: UserRequest):
    try:
        result = run_agent(user_request.query)
        return AgentResponse(
            response=result["response"],
            pros=result["pros"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
