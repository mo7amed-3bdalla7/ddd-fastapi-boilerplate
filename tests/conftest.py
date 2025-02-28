"""
Pytest configuration and shared fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.infrastructure.database.mongodb import get_database
from app.main import app

@pytest.fixture
def test_client():
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)

@pytest.fixture
async def mongo_client():
    """
    Create a test MongoDB client.
    """
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    await client.close()

@pytest.fixture
async def test_database(mongo_client):
    """
    Create a test database and clean it up after tests.
    """
    db = mongo_client["test_db"]
    yield db
    await mongo_client.drop_database("test_db") 