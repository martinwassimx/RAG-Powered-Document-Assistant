from typing import Any, Dict, List, Optional
import httpx
from ollama import Client as OllamaClient

from app.core.config import settings
from app.utils.logging_config import logger

SYSTEM_PROMPT_TEMPLATE = """You are an academic document assistant specializing in University Computer Science materials.
Your task is to answer the user's question accurately and objectively using ONLY the retrieved document context provided below.

Strict Guidelines:
1. Grounding: Rely EXCLUSIVELY on the factual statements in the provided context. Do NOT invent, assume, or extrapolate information.
2. Missing Information: If the provided context does not contain sufficient information to answer the question, state exactly:
   "I could not find this information in the provided documents."
3. Citations: Explicitly cite the document name and page number for each claim made in your response (e.g., "[cs102_operating_systems.pdf, Page 3]").
4. Multiple Sources: When synthesizing information across multiple documents or pages, clearly identify which fact derives from which source.
5. Tone: Maintain a concise, formal, and educational tone.
"""


class GenerationService:
    """Manages prompt engineering and communication with the Ollama LLM."""

    def __init__(self):
        self.host = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.client: Optional[OllamaClient] = None

    def initialize(self) -> None:
        """Initialize the Ollama client."""
        logger.info(f"Initializing Ollama client with host={self.host}, default_model={self.model}")
        self.client = OllamaClient(host=self.host, timeout=self.timeout)

    def check_reachability(self) -> Dict[str, Any]:
        """Verify whether the Ollama server is reachable and inspect installed models."""
        try:
            with httpx.Client(timeout=3.0) as http_client:
                res = http_client.get(f"{self.host.rstrip('/')}/api/tags")
                if res.status_code == 200:
                    models_data = res.json().get("models", [])
                    model_names = [m.get("name") for m in models_data]
                    is_model_present = any(self.model in name for name in model_names)
                    return {
                        "reachable": True,
                        "model": self.model,
                        "installed_models": model_names,
                        "model_ready": is_model_present
                    }
                return {
                    "reachable": False,
                    "error": f"Ollama returned HTTP status {res.status_code}"
                }
        except Exception as exc:
            return {
                "reachable": False,
                "error": f"Connection to Ollama failed: {str(exc)}"
            }

    def build_prompt(self, question: str, context: str) -> str:
        """Construct the prompt sent to the LLM combining context and question."""
        return (
            f"Retrieved Document Context:\n"
            f"----------------------------------------\n"
            f"{context}\n"
            f"----------------------------------------\n\n"
            f"User Question: {question}\n\n"
            f"Please provide a grounded, cited answer based strictly on the context above:"
        )

    def generate_answer(self, question: str, context: str) -> str:
        """Call Ollama LLM to synthesize a grounded answer."""
        if self.client is None:
            self.initialize()

        user_prompt = self.build_prompt(question=question, context=context)

        logger.info(f"Submitting prompt to Ollama model '{self.model}'...")
        try:
            response = self.client.generate(
                model=self.model,
                prompt=user_prompt,
                system=SYSTEM_PROMPT_TEMPLATE,
                options={
                    "temperature": 0.0,  # Zero temperature for deterministic, factual grounding
                    "top_p": 0.9,
                }
            )
            answer = response.get("response", "").strip()
            if not answer:
                answer = "I could not find this information in the provided documents."
            return answer

        except Exception as exc:
            logger.error(f"Error communicating with Ollama: {str(exc)}")
            raise RuntimeError(
                f"Failed to generate answer from Ollama LLM ({self.model}) at {self.host}. "
                f"Detail: {str(exc)}"
            )


# Global singleton instance
generation_service = GenerationService()
