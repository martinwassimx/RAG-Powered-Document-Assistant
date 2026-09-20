import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.generation import generation_service
from app.services.retrieval import retrieval_service


@pytest.fixture(scope="session", autouse=True)
def initialize_services():
    """Ensure services are initialized before running tests."""
    retrieval_service.initialize()
    generation_service.initialize()


@pytest.fixture
def client():
    """Provide TestClient with lifespan context."""
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoint:
    """Tests for GET /health diagnostic endpoint."""

    def test_health_check_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ("healthy", "degraded")
        assert "vector_store" in data
        assert "llm" in data
        assert "embedding_model" in data
        assert data["vector_store"]["initialized"] is True


class TestQueryValidation:
    """Tests for input validation on POST /query (expecting 422)."""

    def test_query_missing_body_returns_422(self, client):
        response = client.post("/query", json={})
        assert response.status_code == 422

    def test_query_empty_string_returns_422(self, client):
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 422

    def test_query_whitespace_only_returns_422(self, client):
        response = client.post("/query", json={"question": "     "})
        assert response.status_code == 422

    def test_query_too_short_returns_422(self, client):
        response = client.post("/query", json={"question": "hi"})
        assert response.status_code == 422

    def test_query_invalid_top_k_returns_422(self, client):
        response = client.post("/query", json={"question": "What is paging?", "top_k": 50})
        assert response.status_code == 422


class TestQueryExecution:
    """Tests for valid execution of POST /query."""

    @patch.object(generation_service, "generate_answer")
    def test_query_happy_path_with_mocked_llm(self, mock_generate, client):
        mock_generate.return_value = (
            "The four Coffman conditions for a deadlock are Mutual Exclusion, "
            "Hold and Wait, No Preemption, and Circular Wait. [cs102_operating_systems.pdf, Page 3]"
        )

        response = client.post("/query", json={
            "question": "What are the four Coffman conditions for a deadlock?",
            "top_k": 3
        })

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)
        assert len(data["sources"]) > 0

        # Verify source metadata
        first_source = data["sources"][0]
        assert "document" in first_source
        assert "page" in first_source
        assert first_source["page"] >= 1
        assert "cs102_operating_systems.pdf" in [s["document"] for s in data["sources"]]

    @patch.object(generation_service, "generate_answer")
    def test_query_retrieves_correct_context(self, mock_generate, client):
        mock_generate.return_value = (
            "TCP establishes connections using a 3-way handshake: SYN, SYN-ACK, and ACK. "
            "[cs104_computer_networks.pdf, Page 2]"
        )

        response = client.post("/query", json={
            "question": "Explain the TCP 3-way handshake process."
        })

        assert response.status_code == 200
        data = response.json()
        assert "TCP" in data["answer"]
        source_docs = [s["document"] for s in data["sources"]]
        assert any("cs104_computer_networks.pdf" in doc for doc in source_docs)


class TestRootEndpoint:
    """Tests for GET / general endpoint."""

    def test_root_returns_welcome_message(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "docs_url" in data
        assert "health_check" in data
