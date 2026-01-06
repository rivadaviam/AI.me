"""Basic usage example for NXO."""

import asyncio
from nxo.core.graph_builder import GraphBuilder
from nxo.core.reasoning_engine import ReasoningEngine
from nxo.integrations.bedrock import BedrockClient
from nxo.integrations.neptune import NeptuneClient
from nxo.audit.audit_logger import AuditLogger


async def main():
    """Example of building a graph and querying it."""
    
    # Initialize clients
    print("Initializing clients...")
    neptune = NeptuneClient()
    bedrock = BedrockClient()
    audit = AuditLogger()
    
    # Initialize core components
    graph_builder = GraphBuilder(neptune)
    reasoning_engine = ReasoningEngine(neptune)
    
    # Step 1: Build a graph from documents
    print("\n1. Building graph from documents...")
    documents = [
        {
            "id": "doc1",
            "title": "Introduction to NXO",
            "content": "NXO is a graph-based metadata infrastructure for Agentic AI. "
                      "It converts documents into semantic graphs and ensures "
                      "grounded responses from LLMs.",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "doc2",
            "title": "Key Features",
            "content": "NXO provides versioning, reasoning, and audit trails. "
                      "It integrates with AWS Bedrock and Neptune.",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
    
    graph_id = await graph_builder.build_from_documents(
        documents=documents,
        metadata={"source": "examples", "version": "1.0"},
        version="v1.0"
    )
    print(f"Graph created: {graph_id}")
    
    # Step 2: Query the graph
    print("\n2. Querying the graph...")
    query = "What is NXO and what are its key features?"
    
    subgraph = await reasoning_engine.get_applicable_subgraph(
        query=query,
        graph_id=graph_id,
        filters={"valid_until": "2024-12-31"}
    )
    print(f"Subgraph extracted: {len(subgraph.get('nodes', []))} nodes, "
          f"{len(subgraph.get('edges', []))} edges")
    
    # Step 3: Generate grounded response
    print("\n3. Generating response with Bedrock...")
    response = await bedrock.generate_response(
        prompt=query,
        context={},
        subgraph=subgraph
    )
    print(f"\nResponse:\n{response['response']}")
    
    # Step 4: Log for audit
    print("\n4. Logging query for audit...")
    audit_id = audit.log_query(
        query=query,
        graph_id=graph_id,
        subgraph=subgraph,
        response=response
    )
    print(f"Audit ID: {audit_id}")
    
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())

