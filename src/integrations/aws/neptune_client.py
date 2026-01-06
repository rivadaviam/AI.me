"""AWS Neptune client for graph storage"""

import logging
from typing import Dict, Any, Optional, List
import boto3
from gremlin_python.driver import client, serializer
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T

logger = logging.getLogger(__name__)


class NeptuneClient:
    """Client for interacting with AWS Neptune"""

    def __init__(
        self,
        endpoint: str,
        port: int = 8182,
        use_ssl: bool = True,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "us-east-1",
    ):
        self.endpoint = endpoint
        self.port = port
        self.use_ssl = use_ssl

        # Create Gremlin client
        connection_string = f"wss://{endpoint}:{port}/gremlin" if use_ssl else f"ws://{endpoint}:{port}/gremlin"

        self.client = client.Client(
            connection_string,
            "g",
            message_serializer=serializer.GraphSONSerializersV2d0(),
        )

        # Store AWS credentials for IAM auth if needed
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name

    def add_vertex(
        self, label: str, properties: Dict[str, Any], vertex_id: Optional[str] = None
    ) -> str:
        """
        Add a vertex to the graph.

        Args:
            label: Vertex label
            properties: Vertex properties
            vertex_id: Optional vertex ID

        Returns:
            Created vertex ID
        """
        try:
            query = f"g.addV('{label}')"
            if vertex_id:
                query += f".property(T.id, '{vertex_id}')"

            for key, value in properties.items():
                if isinstance(value, str):
                    query += f".property('{key}', '{value}')"
                else:
                    query += f".property('{key}', {value})"

            result = self.client.submit(query).all().result()
            return str(result[0].id) if result else vertex_id or ""

        except Exception as e:
            logger.error(f"Error adding vertex: {e}")
            raise

    def add_edge(
        self,
        from_vertex_id: str,
        to_vertex_id: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Add an edge between two vertices.

        Args:
            from_vertex_id: Source vertex ID
            to_vertex_id: Target vertex ID
            label: Edge label
            properties: Optional edge properties

        Returns:
            Created edge ID
        """
        try:
            query = f"g.V('{from_vertex_id}').addE('{label}').to(g.V('{to_vertex_id}'))"

            if properties:
                for key, value in properties.items():
                    if isinstance(value, str):
                        query += f".property('{key}', '{value}')"
                    else:
                        query += f".property('{key}', {value})"

            result = self.client.submit(query).all().result()
            return str(result[0].id) if result else ""

        except Exception as e:
            logger.error(f"Error adding edge: {e}")
            raise

    def query(self, gremlin_query: str) -> List[Any]:
        """
        Execute a Gremlin query.

        Args:
            gremlin_query: Gremlin query string

        Returns:
            Query results
        """
        try:
            result = self.client.submit(gremlin_query).all().result()
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

    def get_vertex(self, vertex_id: str) -> Optional[Dict[str, Any]]:
        """Get a vertex by ID"""
        try:
            query = f"g.V('{vertex_id}').valueMap(true)"
            result = self.client.submit(query).all().result()
            return dict(result[0]) if result else None
        except Exception as e:
            logger.error(f"Error getting vertex: {e}")
            return None

    def get_neighbors(
        self, vertex_id: str, direction: str = "both"
    ) -> List[Dict[str, Any]]:
        """
        Get neighbors of a vertex.

        Args:
            vertex_id: Vertex ID
            direction: 'in', 'out', or 'both'

        Returns:
            List of neighbor vertices
        """
        try:
            if direction == "in":
                query = f"g.V('{vertex_id}').in().valueMap(true)"
            elif direction == "out":
                query = f"g.V('{vertex_id}').out().valueMap(true)"
            else:
                query = f"g.V('{vertex_id}').both().valueMap(true)"

            result = self.client.submit(query).all().result()
            return [dict(r) for r in result]
        except Exception as e:
            logger.error(f"Error getting neighbors: {e}")
            return []

    def close(self):
        """Close the Neptune connection"""
        if self.client:
            self.client.close()

