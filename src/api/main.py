"""FastAPI application main file"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

from src.core.graph.processor import GraphProcessor
from src.core.reasoning.engine import ReasoningEngine
from src.core.versioning.manager import VersionManager
from src.core.audit.logger import AuditLogger
from src.integrations.llm.service import LLMServiceFactory
from src.services.graph_service import GraphService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=os.getenv("LOG_FORMAT", "json"),
)
logger = logging.getLogger(__name__)

# Global service instances
graph_service: Optional[GraphService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    global graph_service

    # Startup
    logger.info("Starting up application...")

    # Initialize core components
    graph_processor = GraphProcessor()
    reasoning_engine = ReasoningEngine()
    version_manager = VersionManager()
    audit_logger = AuditLogger()

    # Initialize LLM service
    llm_service = LLMServiceFactory.create(
        service_type="bedrock",
        region_name=os.getenv("BEDROCK_REGION", "us-east-1"),
        model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Initialize graph service
    graph_service = GraphService(
        graph_processor=graph_processor,
        reasoning_engine=reasoning_engine,
        version_manager=version_manager,
        audit_logger=audit_logger,
        llm_service=llm_service,
    )

    logger.info("Application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="AI.me - Graph-Based Metadata Infrastructure",
    description="Infrastructure for grounded, auditable Agentic AI",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware - use environment variable for allowed origins in production
allowed_origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "*")
allowed_origins = allowed_origins_env.split(",") if allowed_origins_env != "*" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Request/Response models
class DocumentRequest(BaseModel):
    document_id: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = None


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    graph_id: Optional[str] = Field(None, max_length=255)
    filters: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    answer: str
    model: str
    validation: Dict[str, Any]
    subgraph_size: int
    query_event_id: str


class DocumentResponse(BaseModel):
    document_id: str
    graph_version: str
    version_id: str
    status: str


# Dependency to get graph service
def get_graph_service() -> GraphService:
    if graph_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return graph_service


# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI.me - Graph-Based Metadata Infrastructure",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/documents", response_model=DocumentResponse)
async def process_document(
    request: DocumentRequest,
    service: GraphService = Depends(get_graph_service),
):
    """Process a document into a semantic graph"""
    try:
        result = service.process_document(
            document_id=request.document_id,
            content=request.content,
            metadata=request.metadata,
        )
        return DocumentResponse(**result)
    except ValueError as e:
        logger.error(f"Invalid input for document processing: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except ConnectionError as e:
        logger.error(f"Service connection error: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    service: GraphService = Depends(get_graph_service),
):
    """Query the graph and get a grounded response"""
    try:
        result = service.query(
            query=request.query,
            graph_id=request.graph_id,
            filters=request.filters,
        )
        return QueryResponse(**result)
    except ValueError as e:
        logger.error(f"Invalid query input: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid query: {str(e)}")
    except ConnectionError as e:
        logger.error(f"Service connection error during query: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/audit/{session_id}")
async def get_audit_trace(
    session_id: str,
    service: GraphService = Depends(get_graph_service),
):
    """Get audit trace for a session"""
    try:
        trace = service.get_audit_trace(session_id)
        return {"session_id": session_id, "events": trace}
    except ValueError as e:
        logger.error(f"Invalid session ID: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid session ID: {str(e)}")
    except Exception as e:
        logger.error(f"Error getting audit trace: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("API_RELOAD", "true").lower() == "true",
    )

