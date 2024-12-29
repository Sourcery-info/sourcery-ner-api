# Sourcery NER API

This is a simple API for Named Entity Recognition (NER) using Gliner.

## Usage

To run the API, use the following command:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

This will start the server on `http://0.0.0.0:8000`.

## API Documentation

The API documentation is available at `http://localhost:8000/docs`.

## Example Usage

To use the API, send a POST request to `http://localhost:8000/ner` with the following JSON body:

```json
{
  "text": "Mr Jones, CEO of Acme Corp, lives in New York with his wife and two children."
}
```

The response will be a JSON object with the entities and their corresponding labels.
