# Sourcery NER API

This is a simple API for Named Entity Recognition (NER) using Gliner.

## Usage

To run the API, use the following command:

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

This will start the server on `http://0.0.0.0:8000`.

## Docker

To run the API in a Docker container, use the following command:

```bash
docker build -t sourcery-ner-api .
docker run -d -p 8000:8000 sourcery-ner-api
```

OR pull from docker hub:

```bash
docker pull jasony/sourcery-ner-api
docker run -d -p 8000:8000 jasony/sourcery-ner-api
```

## Environment Variables

- `MODEL`: The model to use for entity extraction (default: `EmergentMethods/gliner_large_news-v2.1`).
- `HOST`: The host to run the API on (default: `0.0.0.0`).
- `PORT`: The port to run the API on (default: `8000`).

## API Documentation

The API documentation is available at `http://localhost:8000/docs`.

## Example Usage

To use the API, send a POST request to `http://localhost:8000/ner` with the following JSON body:

```json
{
  "text": "Mr Jones, CEO of Acme Corp, lives in New York with his wife and two children."
}
```

The response will be a JSON object with the entities and their corresponding labels, position in the text, and the score. The score is a float between 0 and 1, where 1 is the highest confidence. Additionally, the response will include the execution time in seconds.

```json
{
  "entities": [
    {
      "start": 0,
      "end": 8,
      "text": "Mr Jones",
      "label": "PERSON",
      "score": 0.9935177564620972
    },
    {
      "start": 17,
      "end": 26,
      "text": "Acme Corp",
      "label": "ORGANIZATION",
      "score": 0.9984927177429199
    },
    {
      "start": 37,
      "end": 45,
      "text": "New York",
      "label": "LOCATION",
      "score": 0.9620553851127625
    }
  ],
  "execution_time": 0.022754430770874023
}
```

## Options

Apart from the `text` field, you can also specify the following optional fields:

- `model`: The model to use for entity extraction (default: `EmergentMethods/gliner_large_news-v2.1`).
- `labels`: The labels to use for entity extraction (default: `['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE']`).
- `threshold`: The threshold to use for entity extraction (default: `0.4`).

## Testing

To test the API, you can use the `test.py` file. This file will send a POST request to the API with the given text and print the response.

```bash
python test.py
```

To run the tests, use the following command:

```bash
pytest
```