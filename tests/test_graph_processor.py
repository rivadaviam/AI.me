"""Tests for graph processor"""

import pytest
from src.core.graph.processor import GraphProcessor


def test_graph_processor_initialization():
    """Test graph processor initialization"""
    processor = GraphProcessor()
    assert processor is not None
    assert processor.graph is not None


def test_process_document():
    """Test document processing"""
    processor = GraphProcessor()
    result = processor.process_document(
        document_id="test-doc-1",
        content="This is a test document",
        metadata={"source": "test"},
    )
    assert result is not None
    assert "test-doc-1" in result


def test_get_subgraph():
    """Test subgraph extraction"""
    processor = GraphProcessor()
    processor.process_document(
        document_id="test-doc-1",
        content="Test content",
    )
    subgraph = processor.get_subgraph("test query")
    assert subgraph is not None

