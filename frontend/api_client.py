import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DEFAULT_API_BASE_URL = "http://localhost:8000"


class APIClient:
    """Client wrapper for communicating with the FastAPI RAG backend."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 90.0):
        # Read from argument, then env variable, then default fallback
        raw_url = base_url or os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
        self.base_url = raw_url.rstrip("/")
        self.timeout = timeout

    def get_health(self) -> Dict[str, Any]:
        """Check backend health and component readiness."""
        url = f"{self.base_url}/health"
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                if response.status_code == 200:
                    return response.json()
                return {
                    "status": "unhealthy",
                    "code": response.status_code,
                    "detail": response.text
                }
        except httpx.ConnectError:
            return {
                "status": "offline",
                "detail": f"Could not connect to backend at {self.base_url}. Ensure FastAPI is running."
            }
        except Exception as exc:
            return {
                "status": "error",
                "detail": f"Health check failed: {str(exc)}"
            }

    def query_document_assistant(self, question: str, top_k: Optional[int] = None) -> Dict[str, Any]:
        """Submit a query to the RAG pipeline."""
        url = f"{self.base_url}/query"
        payload = {"question": question}
        if top_k is not None:
            payload["top_k"] = top_k

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json()
                    }
                elif response.status_code == 422:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error_type": "validation_error",
                        "detail": error_data.get("detail", "Invalid input submitted.")
                    }
                else:
                    return {
                        "success": False,
                        "error_type": "server_error",
                        "status_code": response.status_code,
                        "detail": response.text
                    }
        except httpx.ConnectError:
            return {
                "success": False,
                "error_type": "connection_error",
                "detail": f"Cannot reach the backend server at {self.base_url}. Please verify that the backend is started."
            }
        except httpx.ReadTimeout:
            return {
                "success": False,
                "error_type": "timeout",
                "detail": "The request timed out while awaiting Ollama LLM inference. Consider selecting a faster model or checking GPU availability."
            }
        except Exception as exc:
            return {
                "success": False,
                "error_type": "unexpected_error",
                "detail": f"An unexpected error occurred: {str(exc)}"
            }
