"""Version management for semantic graphs"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class VersionType(Enum):
    """Types of version changes"""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    TEMPORAL = "temporal"


class VersionManager:
    """Manages versions of semantic graphs"""

    def __init__(self):
        self.versions: Dict[str, List[Dict[str, Any]]] = {}

    def create_version(
        self,
        graph_id: str,
        version_type: VersionType = VersionType.TEMPORAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a new version of a graph.

        Args:
            graph_id: Identifier of the graph
            version_type: Type of version change
            metadata: Optional metadata for this version

        Returns:
            Version identifier
        """
        if graph_id not in self.versions:
            self.versions[graph_id] = []

        version_number = len(self.versions[graph_id]) + 1
        version_id = f"{graph_id}:v{version_number}"

        version_data = {
            "version_id": version_id,
            "version_number": version_number,
            "version_type": version_type.value,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
        }

        self.versions[graph_id].append(version_data)
        logger.info(f"Created version {version_id} for graph {graph_id}")

        return version_id

    def get_version(self, graph_id: str, version_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get a specific version or the latest version of a graph.

        Args:
            graph_id: Identifier of the graph
            version_id: Optional specific version identifier

        Returns:
            Version data or None if not found
        """
        if graph_id not in self.versions:
            return None

        versions = self.versions[graph_id]

        if version_id:
            for version in versions:
                if version["version_id"] == version_id:
                    return version
            return None

        # Return latest version
        return versions[-1] if versions else None

    def list_versions(self, graph_id: str) -> List[Dict[str, Any]]:
        """List all versions of a graph"""
        return self.versions.get(graph_id, [])

    def get_temporal_validity(
        self, graph_id: str, version_id: str, timestamp: Optional[datetime] = None
    ) -> bool:
        """
        Check if a version is temporally valid at a given timestamp.

        Args:
            graph_id: Identifier of the graph
            version_id: Version identifier
            timestamp: Timestamp to check (defaults to now)

        Returns:
            True if version is valid at the timestamp
        """
        version = self.get_version(graph_id, version_id)
        if not version:
            return False

        if timestamp is None:
            timestamp = datetime.utcnow()

        created_at = datetime.fromisoformat(version["created_at"])

        # Check if version has expiration
        metadata = version.get("metadata", {})
        expires_at = metadata.get("expires_at")
        if expires_at:
            expires_at = datetime.fromisoformat(expires_at)
            if timestamp > expires_at:
                return False

        # Version is valid if created before or at timestamp
        return created_at <= timestamp

    def compare_versions(
        self, graph_id: str, version_id_1: str, version_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two versions of a graph.

        Args:
            graph_id: Identifier of the graph
            version_id_1: First version identifier
            version_id_2: Second version identifier

        Returns:
            Comparison results
        """
        version_1 = self.get_version(graph_id, version_id_1)
        version_2 = self.get_version(graph_id, version_id_2)

        if not version_1 or not version_2:
            return {"error": "One or both versions not found"}

        return {
            "version_1": version_1,
            "version_2": version_2,
            "differences": self._calculate_differences(version_1, version_2),
        }

    def _calculate_differences(
        self, version_1: Dict[str, Any], version_2: Dict[str, Any]
    ) -> List[str]:
        """Calculate differences between two versions"""
        differences = []

        # Compare metadata
        metadata_1 = version_1.get("metadata", {})
        metadata_2 = version_2.get("metadata", {})

        for key in set(metadata_1.keys()) | set(metadata_2.keys()):
            if key not in metadata_1:
                differences.append(f"Added metadata key: {key}")
            elif key not in metadata_2:
                differences.append(f"Removed metadata key: {key}")
            elif metadata_1[key] != metadata_2[key]:
                differences.append(f"Changed metadata key: {key}")

        return differences

