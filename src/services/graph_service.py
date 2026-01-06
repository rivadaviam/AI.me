"""Service for graph operations"""

import logging
from typing import Dict, Any, Optional, List
from src.core.graph.processor import GraphProcessor
from src.core.reasoning.engine import ReasoningEngine
from src.core.versioning.manager import VersionManager, VersionType
from src.core.audit.logger import AuditLogger, AuditEventType
from src.integrations.llm.service import LLMService

logger = logging.getLogger(__name__)


class GraphService:
    """Service for managing graphs and generating grounded responses"""

    def __init__(
        self,
        graph_processor: GraphProcessor,
        reasoning_engine: ReasoningEngine,
        version_manager: VersionManager,
        audit_logger: AuditLogger,
        llm_service: LLMService,
    ):
        self.graph_processor = graph_processor
        self.reasoning_engine = reasoning_engine
        self.version_manager = version_manager
        self.audit_logger = audit_logger
        self.llm_service = llm_service

    def process_document(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a document into a semantic graph.

        Args:
            document_id: Document identifier
            content: Document content
            metadata: Optional metadata
            user_id: Optional user identifier
            session_id: Optional session identifier

        Returns:
            Processing result with graph version
        """
        # Process document
        graph_version = self.graph_processor.process_document(
            document_id, content, metadata
        )

        # Create version
        version_id = self.version_manager.create_version(
            document_id, VersionType.TEMPORAL, metadata
        )

        # Audit log
        self.audit_logger.log_event(
            AuditEventType.GRAPH_CREATED,
            {
                "document_id": document_id,
                "graph_version": graph_version,
                "version_id": version_id,
            },
            user_id=user_id,
            session_id=session_id,
        )

        return {
            "document_id": document_id,
            "graph_version": graph_version,
            "version_id": version_id,
            "status": "processed",
        }

    def query(
        self,
        query: str,
        graph_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query the graph and generate a grounded response.

        Args:
            query: Query string
            graph_id: Optional specific graph to query
            filters: Optional filters
            user_id: Optional user identifier
            session_id: Optional session identifier

        Returns:
            Response with answer and metadata
        """
        # Audit log query
        query_event_id = self.audit_logger.log_event(
            AuditEventType.LLM_QUERY,
            {"query": query, "graph_id": graph_id, "filters": filters},
            user_id=user_id,
            session_id=session_id,
        )

        # Extract relevant subgraph
        subgraph = self.reasoning_engine.filter_subgraph(
            self.graph_processor.graph, query, filters
        )

        # Validate subgraph
        is_valid, validation_metadata = self.reasoning_engine.validate_subgraph(
            subgraph
        )

        if not is_valid:
            logger.warning(
                f"Subgraph validation failed: {validation_metadata.get('issues')}"
            )

        # Audit log reasoning
        self.audit_logger.log_event(
            AuditEventType.REASONING_EXECUTED,
            {
                "query_event_id": query_event_id,
                "subgraph_size": len(subgraph.nodes),
                "validation": validation_metadata,
            },
            user_id=user_id,
            session_id=session_id,
        )

        # Convert subgraph to context
        context = self._subgraph_to_context(subgraph)

        # Generate response using LLM
        response = self.llm_service.generate(
            prompt=query,
            context=context,
            system_prompt="Answer the question based strictly on the provided context. "
            "If the context doesn't contain enough information, say so.",
        )

        # Audit log response
        self.audit_logger.log_event(
            AuditEventType.LLM_RESPONSE,
            {
                "query_event_id": query_event_id,
                "response_length": len(response.get("text", "")),
                "model": response.get("model"),
            },
            user_id=user_id,
            session_id=session_id,
        )

        return {
            "answer": response.get("text", ""),
            "model": response.get("model"),
            "validation": validation_metadata,
            "subgraph_size": len(subgraph.nodes),
            "query_event_id": query_event_id,
        }

    def _subgraph_to_context(self, subgraph) -> Dict[str, Any]:
        """Convert a NetworkX subgraph to context format for LLM"""
        nodes = []
        edges = []

        for node in subgraph.nodes():
            node_data = subgraph.nodes[node]
            nodes.append({"id": str(node), **node_data})

        for source, target, edge_data in subgraph.edges(data=True):
            edges.append(
                {
                    "source": str(source),
                    "target": str(target),
                    **edge_data,
                }
            )

        return {"nodes": nodes, "edges": edges}

    def get_audit_trace(
        self, session_id: str, user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get complete audit trace for a session"""
        return self.audit_logger.get_trace(session_id)

