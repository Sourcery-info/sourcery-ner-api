from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import argparse
import os
from sourcery_gliner import get_entities, unload_model as unload_reranker
import time

app = FastAPI(title="Sourcery NER API")

# Add API usage instructions
API_INSTRUCTIONS: Dict = {
    "description": "Sourcery NER API - Extracts named entities from text",
    "endpoints": {
        "/": {
            "method": "GET",
            "description": "Returns these API usage instructions"
        },
        "/ner": {
            "method": "POST",
            "description": "Extracts named entities from text",
            "request_body": {
                "text": "string - The text to extract entities from",
                "model": "string - The model to use for entity extraction (default: 'EmergentMethods/gliner_large_news-v2.1')",
                "labels": "array of strings - The labels to use for entity extraction (default: ['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE'])",
                "threshold": "float - The threshold to use for entity extraction (default: 0.4)"
            },
            "response": {
                "entities": "array of objects containing: { start: int, end: int, text: string, label: string, score: float }",
                "execution_time": "float - Time taken to process the request in seconds"
            },
            "example_request": {
                "text": "Mr Jones, CEO of Acme Corp, lives in New York with his wife and two children.",
                "model": "EmergentMethods/gliner_large_news-v2.1",
                "labels": ["PERSON", "ORGANIZATION", "LOCATION", "DATE"],
                "threshold": 0.4
            }
        },
        "/unload": {
            "method": "GET",
            "description": "Unloads the NER model from GPU memory"
        }
    }
}

@app.get("/")
async def root():
    return JSONResponse(content=API_INSTRUCTIONS)

class NERRequest(BaseModel):
    text: str


class EntityResponse(BaseModel):
    start: int
    end: int
    text: str
    label: str
    score: float

class NERResponse(BaseModel):
    entities: List[EntityResponse]
    execution_time: float

@app.post("/ner", response_model=NERResponse)
async def ner_endpoint(request: NERRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    start_time = time.time()
    entities = get_entities(request.text)
    execution_time = time.time() - start_time
    
    return NERResponse(
        entities=entities,
        execution_time=execution_time
    )

@app.get("/unload")
async def unload_model():
    """Unload the model from GPU memory"""
    unload_reranker()
    return {"status": "success", "message": "Model unloaded from memory"}

def get_args():
    parser = argparse.ArgumentParser(description='Document Reranking API Server')
    parser.add_argument('--host', 
                      default=os.environ.get('RERANK_HOST', '0.0.0.0'),
                      help='Host to run the server on (default: 0.0.0.0)')
    parser.add_argument('--port', 
                      type=int,
                      default=int(os.environ.get('RERANK_PORT', '8000')),
                      help='Port to run the server on (default: 8000)')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port) 