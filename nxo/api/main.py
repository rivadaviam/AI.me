"""FastAPI application for NXO."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import structlog

from nxo.config import settings
from nxo.core.graph_builder import GraphBuilder
from nxo.core.reasoning_engine import ReasoningEngine
from nxo.core.versioning import VersionManager
from nxo.integrations.bedrock import BedrockClient
from nxo.integrations.neptune import NeptuneClient
from nxo.audit.audit_logger import AuditLogger

# Initialize structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(settings.log_level),
)

logger = structlog.get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NXO API",
    description="Graph-based metadata infrastructure for Agentic AI",
    version=settings.app_version,
)

# CORS middleware - use environment variable for allowed origins in production
allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize clients (in production, use dependency injection)
# Note: These should be initialized in a dependency injection container
neptune_client = NeptuneClient()
bedrock_client = BedrockClient()
audit_logger = AuditLogger()

graph_builder = GraphBuilder(neptune_client)
reasoning_engine = ReasoningEngine(neptune_client)
# Storage client initialization should be done via dependency injection
# For now, using None as placeholder - this will need proper implementation
version_manager = VersionManager(None)


# Pydantic models for API
class Document(BaseModel):
    """Document model for graph building."""

    id: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    created_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BuildGraphRequest(BaseModel):
    """Request to build a graph from documents."""

    documents: List[Document]
    metadata: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


class QueryRequest(BaseModel):
    """Request to query the graph."""

    query: str = Field(..., min_length=1, max_length=1000, description="User query or question")
    graph_id: str = Field(..., min_length=1, max_length=255, description="ID of the graph to query")
    context: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Response from a query."""

    response: str
    subgraph: Dict[str, Any]
    metadata: Dict[str, Any]
    audit_id: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/graphs", response_model=Dict[str, str])
async def build_graph(request: BuildGraphRequest):
    """
    Build a semantic graph from documents.

    Converts documentation and data into a versioned semantic graph.
    """
    try:
        graph_id = await graph_builder.build_from_documents(
            documents=[doc.dict() for doc in request.documents],
            metadata=request.metadata,
            version=request.version,
        )

        audit_logger.log_graph_operation(
            "create",
            graph_id,
            {"document_count": len(request.documents)},
        )

        return {"graph_id": graph_id, "status": "created"}

    except ValueError as e:
        logger.error("Invalid input for graph building", error=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except ConnectionError as e:
        logger.error("Database connection error", error=str(e))
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error("Failed to build graph", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    """
    Query the graph and generate a grounded response.

    Applies reasoning to get the applicable subgraph, then uses Bedrock
    to generate a response strictly based on that subgraph.
    """
    try:
        # Step 1: Get applicable subgraph
        subgraph = await reasoning_engine.get_applicable_subgraph(
            query=request.query,
            graph_id=request.graph_id,
            context=request.context,
            filters=request.filters,
        )

        # Step 2: Generate response using Bedrock
        response = await bedrock_client.generate_response(
            prompt=request.query,
            context=request.context or {},
            subgraph=subgraph,
        )

        # Step 3: Log for audit
        audit_id = audit_logger.log_query(
            query=request.query,
            graph_id=request.graph_id,
            subgraph=subgraph,
            response=response,
        )

        return QueryResponse(
            response=response["response"],
            subgraph=subgraph,
            metadata=response.get("metadata", {}),
            audit_id=audit_id,
        )

    except ValueError as e:
        logger.error("Invalid query input", error=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid query: {str(e)}")
    except ConnectionError as e:
        logger.error("Database connection error during query", error=str(e))
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error("Query failed", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/graphs/{graph_id}")
async def get_graph(graph_id: str):
    """
    Get information about a graph.
    
    Note: This endpoint is a placeholder. Future implementation should:
    - Retrieve graph metadata from the database
    - Return graph statistics (node count, edge count, etc.)
    - Include version information
    """
    if not graph_id or not graph_id.strip():
        raise HTTPException(status_code=400, detail="Invalid graph_id")
    return {"graph_id": graph_id, "status": "not_implemented"}


@app.put("/graphs/{graph_id}")
async def update_graph(
    graph_id: str,
    updates: Dict[str, Any],
    new_version: Optional[str] = None,
):
    """
    Update a graph and optionally create a new version.
    
    Args:
        graph_id: ID of the graph to update
        updates: Dictionary containing updates (nodes/edges to add/remove)
        new_version: Optional new version identifier
    """
    if not graph_id or not graph_id.strip():
        raise HTTPException(status_code=400, detail="Invalid graph_id")
    try:
        updated_graph_id = await graph_builder.update_graph(
            graph_id=graph_id,
            updates=updates,
            new_version=new_version,
        )

        audit_logger.log_graph_operation(
            "update",
            updated_graph_id,
            {"original_graph_id": graph_id, "updates": updates},
        )

        return {"graph_id": updated_graph_id, "status": "updated"}

    except ValueError as e:
        logger.error("Invalid input for graph update", error=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except ConnectionError as e:
        logger.error("Database connection error during update", error=str(e))
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error("Failed to update graph", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/graphs/{graph_id}/versions")
async def list_versions(graph_id: str):
    """
    List all versions of a graph.
    
    Args:
        graph_id: ID of the graph to list versions for
    """
    if not graph_id or not graph_id.strip():
        raise HTTPException(status_code=400, detail="Invalid graph_id")
    try:
        versions = await version_manager.list_versions(graph_id)
        return {"graph_id": graph_id, "versions": versions}
    except ValueError as e:
        logger.error("Invalid graph_id for version listing", error=str(e))
        raise HTTPException(status_code=400, detail=f"Invalid graph_id: {str(e)}")
    except Exception as e:
        logger.error("Failed to list versions", error=str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "nxo.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )

