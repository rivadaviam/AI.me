"""Audit logger for tracking all operations and decisions."""

from typing import Dict, Any, Optional
from datetime import datetime
import structlog
import json

from nxo.config import settings

logger = structlog.get_logger(__name__)


class AuditLogger:
    """
    Audit logger that records every step for analysis and compliance.

    Ensures full traceability of how responses were generated.
    """

    def __init__(self, storage_client: Optional[Any] = None):
        """
        Initialize the audit logger.

        Args:
            storage_client: Optional client for persistent storage (CloudWatch, S3, etc.)
        """
        self.storage = storage_client
        self.logger = structlog.get_logger(__name__).bind(component="AuditLogger")
        self.enabled = settings.enable_audit

    def log_query(
        self,
        query: str,
        graph_id: str,
        subgraph: Dict[str, Any],
        response: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log a complete query-response cycle.

        Args:
            query: User query
            graph_id: Graph ID used
            subgraph: Subgraph that was used
            response: Generated response
            metadata: Additional metadata

        Returns:
            Audit log ID
        """
        if not self.enabled:
            return ""

        audit_id = f"audit_{datetime.utcnow().isoformat()}"

        audit_entry = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "graph_id": graph_id,
            "subgraph": {
                "node_count": len(subgraph.get("nodes", [])),
                "edge_count": len(subgraph.get("edges", [])),
                "node_ids": [n.get("id") for n in subgraph.get("nodes", [])],
            },
            "response": {
                "text": response.get("response", ""),
                "model": response.get("model"),
                "metadata": response.get("metadata", {}),
            },
            "metadata": metadata or {},
        }

        # Log to structured logger
        self.logger.info("Query logged", audit_id=audit_id, query=query[:100])

        # Store if storage client is available
        if self.storage:
            self._store_audit_entry(audit_id, audit_entry)

        return audit_id

    def log_graph_operation(
        self,
        operation: str,
        graph_id: str,
        details: Dict[str, Any],
    ) -> str:
        """
        Log a graph operation (create, update, delete, etc.).

        Args:
            operation: Type of operation
            graph_id: Graph ID
            details: Operation details

        Returns:
            Audit log ID
        """
        if not self.enabled:
            return ""

        audit_id = f"audit_{datetime.utcnow().isoformat()}"

        audit_entry = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "graph_id": graph_id,
            "details": details,
        }

        self.logger.info("Graph operation logged", audit_id=audit_id, operation=operation)

        if self.storage:
            self._store_audit_entry(audit_id, audit_entry)

        return audit_id

    def log_reasoning_step(
        self,
        step: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        reasoning: Optional[str] = None,
    ) -> str:
        """
        Log a reasoning step for transparency.

        Args:
            step: Name of the reasoning step
            input_data: Input to the step
            output_data: Output from the step
            reasoning: Optional explanation of the reasoning

        Returns:
            Audit log ID
        """
        if not self.enabled:
            return ""

        audit_id = f"audit_{datetime.utcnow().isoformat()}"

        audit_entry = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "input": input_data,
            "output": output_data,
            "reasoning": reasoning,
        }

        self.logger.debug("Reasoning step logged", audit_id=audit_id, step=step)

        if self.storage:
            self._store_audit_entry(audit_id, audit_entry)

        return audit_id

    def _store_audit_entry(self, audit_id: str, entry: Dict[str, Any]) -> None:
        """
        Store audit entry in persistent storage.
        
        Args:
            audit_id: Unique identifier for the audit entry
            entry: Dictionary containing audit entry data
            
        Note: CloudWatch and S3 storage implementations are placeholders.
        Future enhancements should implement proper AWS service integration.
        """
        if not self.storage:
            return

        try:
            storage_type = settings.audit_storage_type.lower()
            if storage_type == "cloudwatch":
                # Note: CloudWatch logging implementation needed
                # Should use boto3 CloudWatch Logs client
                self.logger.warning("CloudWatch storage not yet implemented, using local storage")
                self._store_local(audit_id, entry)
            elif storage_type == "s3":
                # Note: S3 storage implementation needed
                # Should use boto3 S3 client to store JSON files
                self.logger.warning("S3 storage not yet implemented, using local storage")
                self._store_local(audit_id, entry)
            else:
                # Local file storage
                self._store_local(audit_id, entry)
        except OSError as e:
            self.logger.error("Failed to store audit entry (filesystem error)", audit_id=audit_id, error=str(e))
        except Exception as e:
            self.logger.error("Failed to store audit entry", audit_id=audit_id, error=str(e), exc_info=True)

    def _store_local(self, audit_id: str, entry: Dict[str, Any]) -> None:
        """
        Store audit entry locally (for development).
        
        Args:
            audit_id: Unique identifier for the audit entry
            entry: Dictionary containing audit entry data
        """
        import os

        audit_dir = "logs/audit"
        try:
            os.makedirs(audit_dir, exist_ok=True)
        except OSError as e:
            self.logger.error("Failed to create audit directory", directory=audit_dir, error=str(e))
            raise

        # Sanitize audit_id for filesystem safety
        safe_audit_id = "".join(c for c in audit_id if c.isalnum() or c in "._-")
        filepath = os.path.join(audit_dir, f"{safe_audit_id}.json")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)
        except OSError as e:
            self.logger.error("Failed to write audit file", filepath=filepath, error=str(e))
            raise

