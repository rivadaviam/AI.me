"""Reasoning engine that filters and validates applicable subgraphs"""

import logging
from typing import Dict, List, Optional, Any, Tuple
import networkx as nx

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """Engine for reasoning about graph validity and applicability"""

    def __init__(self, validation_rules: Optional[List[Dict[str, Any]]] = None):
        self.validation_rules = validation_rules or []
        self.groundedness_threshold = 0.7

    def validate_subgraph(
        self, subgraph: nx.MultiDiGraph, context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate a subgraph for applicability and groundedness.

        Args:
            subgraph: The subgraph to validate
            context: Optional context information

        Returns:
            Tuple of (is_valid, validation_metadata)
        """
        logger.info(f"Validating subgraph with {len(subgraph.nodes)} nodes")

        validation_results = {
            "is_valid": True,
            "groundedness_score": 0.0,
            "issues": [],
            "warnings": [],
        }

        # Check graph structure
        if len(subgraph.nodes) == 0:
            validation_results["is_valid"] = False
            validation_results["issues"].append("Empty subgraph")
            return False, validation_results

        # Calculate groundedness score
        groundedness = self._calculate_groundedness(subgraph, context)
        validation_results["groundedness_score"] = groundedness

        if groundedness < self.groundedness_threshold:
            validation_results["is_valid"] = False
            validation_results["issues"].append(
                f"Groundedness score {groundedness:.2f} below threshold "
                f"{self.groundedness_threshold}"
            )

        # Apply validation rules
        for rule in self.validation_rules:
            rule_result = self._apply_validation_rule(subgraph, rule, context)
            if not rule_result["passed"]:
                validation_results["is_valid"] = False
                validation_results["issues"].extend(rule_result.get("issues", []))

        validation_results["is_valid"] = (
            validation_results["is_valid"]
            and groundedness >= self.groundedness_threshold
        )

        return validation_results["is_valid"], validation_results

    def _calculate_groundedness(
        self, subgraph: nx.MultiDiGraph, context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculate groundedness score for the subgraph.

        Groundedness measures how well the subgraph is connected to
        verified sources and how complete the information is.
        """
        if len(subgraph.nodes) == 0:
            return 0.0

        # Calculate based on:
        # 1. Node metadata completeness
        # 2. Edge connectivity
        # 3. Source verification
        metadata_score = self._score_metadata_completeness(subgraph)
        connectivity_score = self._score_connectivity(subgraph)
        verification_score = self._score_source_verification(subgraph)

        # Weighted average
        groundedness = (
            0.4 * metadata_score + 0.3 * connectivity_score + 0.3 * verification_score
        )

        return min(1.0, max(0.0, groundedness))

    def _score_metadata_completeness(self, subgraph: nx.MultiDiGraph) -> float:
        """Score how complete the metadata is for nodes"""
        if len(subgraph.nodes) == 0:
            return 0.0

        total_score = 0.0
        for node in subgraph.nodes():
            node_data = subgraph.nodes[node]
            # Check for required metadata fields
            required_fields = ["source", "timestamp"]
            present_fields = sum(1 for field in required_fields if field in node_data)
            total_score += present_fields / len(required_fields)

        return total_score / len(subgraph.nodes)

    def _score_connectivity(self, subgraph: nx.MultiDiGraph) -> float:
        """Score how well connected the subgraph is"""
        if len(subgraph.nodes) == 0:
            return 0.0

        # Check if graph is connected
        if nx.is_weakly_connected(subgraph):
            connectivity = 1.0
        else:
            # Calculate connectivity ratio
            components = list(nx.weakly_connected_components(subgraph))
            largest_component_size = max(len(c) for c in components) if components else 0
            connectivity = largest_component_size / len(subgraph.nodes)

        return connectivity

    def _score_source_verification(self, subgraph: nx.MultiDiGraph) -> float:
        """Score how well verified the sources are"""
        if len(subgraph.nodes) == 0:
            return 0.0

        verified_count = 0
        for node in subgraph.nodes():
            node_data = subgraph.nodes[node]
            if node_data.get("verified", False):
                verified_count += 1

        return verified_count / len(subgraph.nodes)

    def _apply_validation_rule(
        self,
        subgraph: nx.MultiDiGraph,
        rule: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Apply a validation rule to the subgraph"""
        rule_type = rule.get("type")
        result = {"passed": True, "issues": []}

        # TODO: Implement specific rule types
        # Examples: temporal_validity, completeness, consistency

        return result

    def filter_subgraph(
        self,
        graph: nx.MultiDiGraph,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> nx.MultiDiGraph:
        """
        Filter a graph to get applicable subgraph based on query.

        Args:
            graph: Full graph to filter
            query: Query string
            filters: Optional filters

        Returns:
            Filtered subgraph
        """
        logger.info(f"Filtering graph with query: {query}")

        # TODO: Implement semantic filtering based on query
        # For now, return a copy of the graph
        subgraph = graph.copy()

        # Apply filters if provided
        if filters:
            nodes_to_keep = set()
            for node in graph.nodes():
                node_data = graph.nodes[node]
                if self._node_matches_filters(node_data, filters):
                    nodes_to_keep.add(node)

            subgraph = graph.subgraph(nodes_to_keep).copy()

        return subgraph

    def _node_matches_filters(
        self, node_data: Dict[str, Any], filters: Dict[str, Any]
    ) -> bool:
        """Check if a node matches the given filters"""
        for key, value in filters.items():
            if key not in node_data:
                return False
            if node_data[key] != value:
                return False
        return True

