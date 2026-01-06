"""Example usage of AI.me Graph Service"""

import asyncio
import os
from dotenv import load_dotenv

from src.core.graph.processor import GraphProcessor
from src.core.reasoning.engine import ReasoningEngine
from src.core.versioning.manager import VersionManager, VersionType
from src.core.audit.logger import AuditLogger
from src.integrations.llm.service import LLMServiceFactory
from src.services.graph_service import GraphService

# Load environment variables
load_dotenv()


def main():
    """Example usage of the graph service"""

    print("🚀 Initializing AI.me Graph Service...")

    # Initialize components
    graph_processor = GraphProcessor()
    reasoning_engine = ReasoningEngine()
    version_manager = VersionManager()
    audit_logger = AuditLogger()

    # Initialize LLM service (requires AWS credentials)
    try:
        llm_service = LLMServiceFactory.create(
            service_type="bedrock",
            region_name=os.getenv("BEDROCK_REGION", "us-east-1"),
            model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        print("✅ LLM Service initialized")
    except Exception as e:
        print(f"⚠️  Could not initialize LLM service: {e}")
        print("   Continuing without LLM (queries will not work)")
        llm_service = None

    # Create graph service
    if llm_service:
        graph_service = GraphService(
            graph_processor=graph_processor,
            reasoning_engine=reasoning_engine,
            version_manager=version_manager,
            audit_logger=audit_logger,
            llm_service=llm_service,
        )
    else:
        print("⚠️  Graph service created without LLM")
        return

    # Example: Process a document
    print("\n📄 Processing document...")
    document_result = graph_service.process_document(
        document_id="example-doc-1",
        content="""
        Artificial Intelligence (AI) is a branch of computer science that focuses
        on creating systems capable of performing tasks that normally require
        human intelligence. Autonomous agents are AI systems that can
        operate independently to achieve specific objectives.
        """,
        metadata={
            "source": "example",
            "author": "AI.me Team",
            "topic": "AI",
        },
        session_id="example-session-1",
    )
    print(f"✅ Document processed: {document_result['graph_version']}")

    # Example: Query the graph
    if llm_service:
        print("\n❓ Querying graph...")
        query_result = graph_service.query(
            query="What is artificial intelligence?",
            session_id="example-session-1",
        )
        print(f"✅ Answer: {query_result['answer']}")
        print(f"   Groundedness: {query_result['validation']['groundedness_score']:.2f}")

    # Example: Get audit trace
    print("\n📊 Getting audit trace...")
    trace = graph_service.get_audit_trace("example-session-1")
    print(f"✅ Found {len(trace)} audit events")
    for event in trace:
        print(f"   - {event['event_type']}: {event['timestamp']}")

    print("\n✅ Example completed!")


if __name__ == "__main__":
    main()
