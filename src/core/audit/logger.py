"""Audit logging system for tracking operations"""

import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events"""

    GRAPH_CREATED = "graph_created"
    GRAPH_UPDATED = "graph_updated"
    GRAPH_VERSIONED = "graph_versioned"
    SUBGRAPH_EXTRACTED = "subgraph_extracted"
    SUBGRAPH_VALIDATED = "subgraph_validated"
    LLM_QUERY = "llm_query"
    LLM_RESPONSE = "llm_response"
    REASONING_EXECUTED = "reasoning_executed"
    ERROR = "error"


class AuditLogger:
    """Logs audit events for compliance and analysis"""

    def __init__(self, storage_backend: Optional[Any] = None):
        self.storage_backend = storage_backend
        self.events: List[Dict[str, Any]] = []

    def log_event(
        self,
        event_type: AuditEventType,
        details: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> str:
        """
        Log an audit event.

        Args:
            event_type: Type of event
            details: Event details
            user_id: Optional user identifier
            session_id: Optional session identifier

        Returns:
            Event identifier
        """
        event = {
            "event_id": self._generate_event_id(),
            "event_type": event_type.value,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "session_id": session_id,
            "details": details,
        }

        self.events.append(event)

        # Log to standard logger
        logger.info(
            f"Audit event: {event_type.value}",
            extra={"audit_event": json.dumps(event)},
        )

        # Store in backend if available
        if self.storage_backend:
            self._store_event(event)

        return event["event_id"]

    def _generate_event_id(self) -> str:
        """Generate a unique event identifier"""
        timestamp = datetime.utcnow().timestamp()
        return f"event_{int(timestamp * 1000000)}"

    def _store_event(self, event: Dict[str, Any]):
        """Store event in backend"""
        # TODO: Implement backend storage (database, S3, etc.)
        pass

    def get_events(
        self,
        event_type: Optional[AuditEventType] = None,
        user_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve audit events with filters.

        Args:
            event_type: Optional event type filter
            user_id: Optional user filter
            start_time: Optional start time filter
            end_time: Optional end time filter
            limit: Maximum number of events to return

        Returns:
            List of matching events
        """
        filtered_events = self.events

        if event_type:
            filtered_events = [
                e for e in filtered_events if e["event_type"] == event_type.value
            ]

        if user_id:
            filtered_events = [
                e for e in filtered_events if e.get("user_id") == user_id
            ]

        if start_time:
            filtered_events = [
                e
                for e in filtered_events
                if datetime.fromisoformat(e["timestamp"]) >= start_time
            ]

        if end_time:
            filtered_events = [
                e
                for e in filtered_events
                if datetime.fromisoformat(e["timestamp"]) <= end_time
            ]

        # Sort by timestamp descending
        filtered_events.sort(
            key=lambda x: x["timestamp"], reverse=True
        )

        return filtered_events[:limit]

    def get_trace(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get complete trace of events for a session.

        Args:
            session_id: Session identifier

        Returns:
            List of events in chronological order
        """
        events = [
            e for e in self.events if e.get("session_id") == session_id
        ]
        events.sort(key=lambda x: x["timestamp"])
        return events

