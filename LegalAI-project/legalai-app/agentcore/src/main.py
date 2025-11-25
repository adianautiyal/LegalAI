"""
LegalAI AgentCore Runtime - Main FastAPI application
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import chat, health, tools, legal_services
from .agent.legal_agent import LegalAgent
from .models.schemas import ChatRequest, ChatResponse, HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global agent instances cache
agent_cache: Dict[str, LegalAgent] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting LegalAI AgentCore Runtime")
    
    # Initialize any required services here
    yield
    
    # Cleanup
    logger.info("Shutting down LegalAI AgentCore Runtime")
    agent_cache.clear()

# Create FastAPI application
app = FastAPI(
    title="LegalAI AgentCore Runtime",
    description="AI-powered legal automation platform with AWS Bedrock AgentCore",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(legal_services.router, prefix="/legal", tags=["legal"])

def get_legal_agent(session_id: str, user_id: str) -> LegalAgent:
    """
    Get or create a LegalAgent instance for the session
    """
    cache_key = f"{user_id}:{session_id}"
    
    if cache_key not in agent_cache:
        memory_arn = os.getenv("AGENTCORE_MEMORY_ARN")
        if not memory_arn:
            raise HTTPException(
                status_code=500,
                detail="AgentCore Memory ARN not configured"
            )
        
        agent_cache[cache_key] = LegalAgent(
            session_id=session_id,
            user_id=user_id,
            memory_arn=memory_arn
        )
        logger.info(f"Created new LegalAgent for session {session_id}")
    
    return agent_cache[cache_key]

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "service": "LegalAI AgentCore Runtime",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/chat/stream", response_model=ChatResponse)
async def chat_stream(request: ChatRequest):
    """
    Stream chat endpoint for legal queries
    """
    try:
        agent = get_legal_agent(request.session_id, request.user_id)
        
        response = await agent.process_legal_query(
            query=request.message,
            context=request.context
        )
        
        return ChatResponse(
            response=response.get("response", ""),
            session_id=request.session_id,
            user_id=request.user_id,
            metadata=response
        )
        
    except Exception as e:
        logger.error(f"Error in chat stream: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/legal/analyze-contract")
async def analyze_contract(
    session_id: str,
    user_id: str,
    document_content: str,
    contract_type: str = "general"
):
    """
    Analyze a legal contract
    """
    try:
        agent = get_legal_agent(session_id, user_id)
        
        analysis = await agent.analyze_contract(
            document_content=document_content,
            contract_type=contract_type
        )
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in contract analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/legal/research")
async def legal_research(
    session_id: str,
    user_id: str,
    legal_question: str,
    jurisdiction: str = "federal"
):
    """
    Conduct legal research
    """
    try:
        agent = get_legal_agent(session_id, user_id)
        
        research = await agent.research_legal_issue(
            legal_question=legal_question,
            jurisdiction=jurisdiction
        )
        
        return research
        
    except Exception as e:
        logger.error(f"Error in legal research: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )