"""
Minimal integration test for API ping endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for FastAPI app."""
    return TestClient(app)


def test_ping(client):
    """Test that the ping endpoint returns a successful response."""
    response = client.get("/ping")

    assert response.is_success
    assert response.json() == {"ping": "pong"}
