"""Tests for reasoning engine"""

import pytest
import networkx as nx
from src.core.reasoning.engine import ReasoningEngine


def test_reasoning_engine_initialization():
    """Test reasoning engine initialization"""
    engine = ReasoningEngine()
    assert engine is not None
    assert engine.groundedness_threshold == 0.7


def test_validate_subgraph():
    """Test subgraph validation"""
    engine = ReasoningEngine()
    subgraph = nx.MultiDiGraph()
    subgraph.add_node("node1", source="test", timestamp="2024-01-01", verified=True)
    subgraph.add_node("node2", source="test", timestamp="2024-01-01", verified=True)
    subgraph.add_edge("node1", "node2", relationship="related")

    is_valid, metadata = engine.validate_subgraph(subgraph)
    assert isinstance(is_valid, bool)
    assert "groundedness_score" in metadata


def test_filter_subgraph():
    """Test subgraph filtering"""
    engine = ReasoningEngine()
    graph = nx.MultiDiGraph()
    graph.add_node("node1", type="document")
    graph.add_node("node2", type="entity")

    subgraph = engine.filter_subgraph(graph, "test query", filters={"type": "document"})
    assert subgraph is not None

