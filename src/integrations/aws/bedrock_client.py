"""AWS Bedrock client for LLM integration"""

import logging
from typing import Dict, Any, Optional, List
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BedrockClient:
    """Client for interacting with AWS Bedrock"""

    def __init__(
        self,
        region_name: str = "us-east-1",
        model_id: str = "anthropic.claude-v2",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.region_name = region_name
        self.model_id = model_id

        session_kwargs = {"region_name": region_name}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs.update(
                {
                    "aws_access_key_id": aws_access_key_id,
                    "aws_secret_access_key": aws_secret_access_key,
                }
            )

        self.bedrock_runtime = boto3.client("bedrock-runtime", **session_kwargs)
        self.bedrock = boto3.client("bedrock", **session_kwargs)

    def invoke_model(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Invoke a Bedrock model with a prompt.

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            context: Optional context from subgraph

        Returns:
            Model response
        """
        try:
            # Build the prompt with context if provided
            full_prompt = self._build_prompt(prompt, system_prompt, context)

            # Prepare request body based on model
            if "claude" in self.model_id:
                body = self._prepare_claude_request(
                    full_prompt, max_tokens, temperature, top_p
                )
            else:
                # Generic format for other models
                body = {
                    "prompt": full_prompt,
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    "topP": top_p,
                }

            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id, body=body
            )

            response_body = response.get("body").read()
            result = self._parse_response(response_body)

            logger.info(f"Successfully invoked model {self.model_id}")
            return result

        except ClientError as e:
            logger.error(f"Error invoking Bedrock model: {e}")
            raise

    def _build_prompt(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build the full prompt with system prompt and context"""
        parts = []

        if system_prompt:
            parts.append(f"System: {system_prompt}")

        if context:
            context_str = self._format_context(context)
            parts.append(f"Context:\n{context_str}")

        parts.append(f"User: {prompt}")

        return "\n\n".join(parts)

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context from subgraph into prompt"""
        # Extract relevant information from context
        # This should be based on the subgraph structure
        if "nodes" in context:
            nodes_info = "\n".join(
                [f"- {node.get('id', 'unknown')}: {node.get('data', {})}" for node in context["nodes"]]
            )
            return f"Relevant Information:\n{nodes_info}"
        return str(context)

    def _prepare_claude_request(
        self, prompt: str, max_tokens: int, temperature: float, top_p: float
    ) -> Dict[str, Any]:
        """Prepare request body for Claude models"""
        import json

        return json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            }
        )

    def _parse_response(self, response_body: bytes) -> Dict[str, Any]:
        """Parse the response from Bedrock"""
        import json

        response_json = json.loads(response_body)

        # Handle different response formats
        if "content" in response_json:
            # Claude format
            content = response_json["content"]
            text = content[0]["text"] if content else ""
            return {
                "text": text,
                "raw_response": response_json,
            }
        elif "completion" in response_json:
            # Other models
            return {
                "text": response_json["completion"],
                "raw_response": response_json,
            }
        else:
            return {
                "text": str(response_json),
                "raw_response": response_json,
            }

    def list_models(self) -> List[Dict[str, Any]]:
        """List available Bedrock models"""
        try:
            response = self.bedrock.list_foundation_models()
            return response.get("modelSummaries", [])
        except ClientError as e:
            logger.error(f"Error listing Bedrock models: {e}")
            return []

