import pytest
from fastapi.testclient import TestClient
from api import app, API_INSTRUCTIONS
from unittest.mock import patch
from sourcery_gliner import get_entities, load_model, unload_model
client = TestClient(app)

# Test data
TEST_TEXT = "Mr Jones, CEO of Acme Corp, lives in New York with his wife and two children."
TEST_MODEL = "EmergentMethods/gliner_large_news-v2.1"
TEST_LABELS = ["PERSON", "ORGANIZATION", "LOCATION", "DATE"]
TEST_THRESHOLD = 0.4


def test_root_endpoint():
    """Test the root endpoint returns API instructions"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == API_INSTRUCTIONS

def test_ner_endpoint_success():
    """Test successful NER"""
    request_data = {
        "text": TEST_TEXT,
        "model": TEST_MODEL,
        "labels": TEST_LABELS,
        "threshold": TEST_THRESHOLD
    }
    
    response = client.post("/ner", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    
    assert "entities" in data
    assert "execution_time" in data
    assert len(data["entities"]) == 2
    
    # Check response structure
    first_doc = data["entities"][0]
    assert "entity" in first_doc
    assert "type" in first_doc
    assert isinstance(first_doc["type"], str)

def test_unload_endpoint():
    """Test the model unload endpoint"""
    with patch('api.unload_model') as mock_unload:
        response = client.get("/unload")
        
        # Check response
        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "message": "Model unloaded from memory"
        }
        
        # Verify unload_model was called
        mock_unload.assert_called_once()
