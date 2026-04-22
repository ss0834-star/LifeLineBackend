# API Evaluation Platform Backend

This is a complete, minimal, and deployment-ready Python backend for an API evaluation platform.
It provides a public endpoint to answer arithmetic questions provided in a natural language query.

## Project Purpose
To parse and solve basic arithmetic operations (+, -, *, /) from natural language strings via a robust API endpoint.

## GET /
Returns a health check message.
```json
{
  "message": "API is running"
}
```

## POST /v1/answer
The evaluator endpoint.
### Request Format
```json
{
  "query": "What is 10 + 15?",
  "assets": []
}
```

### Response Format
```json
{
  "output": "The sum is 25."
}
```

## Local Run Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server locally:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Example cURL
```bash
curl -X POST "http://127.0.0.1:8000/v1/answer" \
-H "Content-Type: application/json" \
-d '{"query":"What is 10 + 15?","assets":[]}'
```

## Deployment Note
The final submit URL should be:
`https://your-domain.com/v1/answer`
