# Agent Context

## System Overview

AI.me is a graph-based metadata infrastructure for Agentic AI. The system converts documents into semantic graphs, validates subgraphs, and generates grounded responses using LLM services.

## Core Components

1. **GraphProcessor**: Converts documents to graphs
2. **ReasoningEngine**: Validates and filters subgraphs
3. **VersionManager**: Manages graph versions
4. **AuditLogger**: Logs all operations
5. **GraphService**: Orchestrates components
6. **LLMService**: Integrates with LLM providers

## Key Concepts

- **Graph**: Semantic representation of knowledge
- **Subgraph**: Relevant portion of graph for a query
- **Groundedness**: Measure of response reliability
- **Versioning**: Temporal tracking of graph changes
- **Audit Trail**: Complete operation logging

## Agent Capabilities

Agents can:
- Process documents into graphs
- Query graphs for information
- Validate subgraphs
- Generate grounded responses
- Access audit trails

## References

- Agent Capabilities: `docs/agents/AGENT_CAPABILITIES.md`
- Agent Constraints: `docs/agents/AGENT_CONSTRAINTS.md`

