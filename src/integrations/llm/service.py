"""LLM service abstraction layer"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMService(ABC):
    """Abstract base class for LLM services"""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt
            context: Optional context from subgraph
            **kwargs: Additional parameters

        Returns:
            Generated response
        """
        pass


class LLMServiceFactory:
    """Factory for creating LLM service instances"""

    @staticmethod
    def create(
        service_type: str = "bedrock", **kwargs: Any
    ) -> LLMService:
        """
        Create an LLM service instance.

        Args:
            service_type: Type of service ('bedrock', 'openai', etc.)
            **kwargs: Service-specific configuration

        Returns:
            LLM service instance
        """
        if service_type == "bedrock":
            from src.integrations.aws.bedrock_client import BedrockClient

            return BedrockLLMService(BedrockClient(**kwargs))
        elif service_type == "openai":
            # TODO: Implement OpenAI service
            raise NotImplementedError("OpenAI service not yet implemented")
        else:
            raise ValueError(f"Unknown LLM service type: {service_type}")


class BedrockLLMService(LLMService):
    """LLM service implementation using AWS Bedrock"""

    def __init__(self, bedrock_client):
        self.bedrock_client = bedrock_client

    def generate(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate response using Bedrock"""
        system_prompt = (
            system_prompt
            or "You are a helpful AI assistant. Answer questions based strictly on the provided context."
        )

        response = self.bedrock_client.invoke_model(
            prompt=prompt,
            system_prompt=system_prompt,
            context=context,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )

        return {
            "text": response.get("text", ""),
            "model": self.bedrock_client.model_id,
            "raw_response": response.get("raw_response"),
        }

