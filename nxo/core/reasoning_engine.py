"""Reasoning engine that filters and validates applicable subgraphs."""

from typing import Dict, List, Any, Optional
import structlog

logger = structlog.get_logger(__name__)


class ReasoningEngine:
    """
    Applies reasoning to filter and validate the applicable subgraph for each query.

    This engine ensures that only relevant, validated, and temporally correct
    information is used for generating responses.
    """

    def __init__(self, graph_db_client: Any):
        """
        Initialize the reasoning engine.

        Args:
            graph_db_client: Client for the graph database
        """
        self.graph_db = graph_db_client
        self.logger = logger.bind(component="ReasoningEngine")

    async def get_applicable_subgraph(
        self,
        query: str,
        graph_id: str,
        context: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get the applicable subgraph for a given query.

        Args:
            query: The user query/question
            graph_id: ID of the graph to query
            context: Additional context for reasoning
            filters: Filters to apply (temporal, validity, etc.)

        Returns:
            Dictionary containing the subgraph (nodes and edges)
        """
        # Log query with length limit for security and performance
        QUERY_LOG_MAX_LENGTH = 100
        query_preview = query[:QUERY_LOG_MAX_LENGTH] if len(query) > QUERY_LOG_MAX_LENGTH else query
        self.logger.info(
            "Getting applicable subgraph",
            query=query_preview,
            query_length=len(query),
            graph_id=graph_id,
        )

        # Step 1: Extract query intent and key concepts
        query_concepts = await self._extract_query_concepts(query)

        # Step 2: Find relevant nodes in the graph
        relevant_nodes = await self._find_relevant_nodes(graph_id, query_concepts)

        # Step 3: Apply filters (temporal, validity, etc.)
        if filters:
            relevant_nodes = await self._apply_filters(relevant_nodes, filters)

        # Step 4: Expand to include related nodes (subgraph)
        subgraph = await self._expand_subgraph(graph_id, relevant_nodes, max_depth=2)

        # Step 5: Validate subgraph completeness and consistency
        validated_subgraph = await self._validate_subgraph(subgraph, query)

        self.logger.info(
            "Subgraph extracted",
            node_count=len(validated_subgraph.get("nodes", [])),
            edge_count=len(validated_subgraph.get("edges", [])),
        )

        return validated_subgraph

    async def _extract_query_concepts(self, query: str) -> List[str]:
        """
        Extract key concepts from the query.

        Note: This is a placeholder implementation. In production, this should use
        NLP/LLM to identify entities and concepts for better semantic understanding.
        
        Args:
            query: The query string to extract concepts from
            
        Returns:
            List of extracted concept strings
        """
        if not query or not query.strip():
            return []
        # Placeholder: Simple keyword extraction
        # In production, this would use entity recognition, semantic analysis, etc.
        concepts = [c.strip() for c in query.lower().split() if c.strip()]
        return concepts

    async def _find_relevant_nodes(
        self, graph_id: str, concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Find nodes in the graph that match the query concepts.
        
        Args:
            graph_id: ID of the graph to search
            concepts: List of concept strings to search for
            
        Returns:
            List of matching node dictionaries
        """
        if not concepts:
            return []
            
        nodes = []
        seen_node_ids = set()  # Prevent duplicate nodes
        
        for concept in concepts:
            if not concept:
                continue
            try:
                matching_nodes = await self.graph_db.search_nodes(graph_id, concept)
                for node in matching_nodes:
                    node_id = node.get("id")
                    if node_id and node_id not in seen_node_ids:
                        nodes.append(node)
                        seen_node_ids.add(node_id)
            except Exception as e:
                self.logger.warning(
                    "Error searching for concept",
                    concept=concept,
                    error=str(e),
                )
                continue
                
        return nodes

    async def _apply_filters(
        self, nodes: List[Dict[str, Any]], filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Apply filters to nodes (temporal validity, data freshness, etc.).

        Args:
            nodes: List of nodes to filter
            filters: Dictionary of filter criteria

        Returns:
            Filtered list of nodes
        """
        filtered_nodes = nodes

        # Temporal filter
        if "valid_until" in filters:
            valid_until = filters["valid_until"]
            filtered_nodes = [
                n
                for n in filtered_nodes
                if n.get("properties", {}).get("valid_until") is None
                or n["properties"]["valid_until"] > valid_until
            ]

        # Type filter
        if "node_types" in filters:
            allowed_types = filters["node_types"]
            filtered_nodes = [
                n for n in filtered_nodes if n.get("type") in allowed_types
            ]

        # Source filter
        if "sources" in filters:
            allowed_sources = filters["sources"]
            filtered_nodes = [
                n
                for n in filtered_nodes
                if n.get("properties", {}).get("source") in allowed_sources
            ]

        return filtered_nodes

    async def _expand_subgraph(
        self, graph_id: str, seed_nodes: List[Dict[str, Any]], max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        Expand seed nodes into a connected subgraph.

        Args:
            graph_id: ID of the graph
            seed_nodes: Initial nodes to expand from
            max_depth: Maximum depth to expand

        Returns:
            Dictionary with 'nodes' and 'edges' keys
        """
        subgraph_nodes = {node["id"]: node for node in seed_nodes}
        subgraph_edges = []

        # Expand by following edges from seed nodes
        current_level = seed_nodes
        for depth in range(max_depth):
            next_level = []
            for node in current_level:
                edges = await self.graph_db.get_node_edges(graph_id, node["id"])
                for edge in edges:
                    subgraph_edges.append(edge)
                    # Add connected nodes
                    connected_node_id = (
                        edge["target"] if edge["source"] == node["id"] else edge["source"]
                    )
                    if connected_node_id not in subgraph_nodes:
                        connected_node = await self.graph_db.get_node(
                            graph_id, connected_node_id
                        )
                        if connected_node:
                            subgraph_nodes[connected_node_id] = connected_node
                            next_level.append(connected_node)
            current_level = next_level
            if not current_level:
                break

        return {
            "nodes": list(subgraph_nodes.values()),
            "edges": subgraph_edges,
        }

    async def _validate_subgraph(
        self, subgraph: Dict[str, Any], query: str
    ) -> Dict[str, Any]:
        """
        Validate that the subgraph is complete and consistent.

        Args:
            subgraph: The subgraph to validate
            query: Original query for context

        Returns:
            Validated (and potentially enriched) subgraph
            
        Note: This is a placeholder implementation. Future enhancements should include:
        - Check for missing connections
        - Verify data consistency
        - Ensure temporal coherence
        - Validate against query requirements
        """
        if not subgraph:
            self.logger.warning("Empty subgraph provided for validation")
            return {"nodes": [], "edges": []}
        
        # Basic validation: ensure required keys exist
        if "nodes" not in subgraph:
            subgraph["nodes"] = []
        if "edges" not in subgraph:
            subgraph["edges"] = []
            
        return subgraph

