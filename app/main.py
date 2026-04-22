import json
from fastapi import FastAPI, Request, Response
from app.routes.answer import router as answer_router

app = FastAPI(title="API Evaluation Platform Backend")

# Global handler for character-perfect JSON serialization
def create_raw_json_response(data: dict):
    # separators=(',', ':') removes all whitespace between keys and values
    # ensuring the output is strictly '{"output":"10"}' with ZERO extra characters.
    json_str = json.dumps(data, separators=(',', ':'))
    return Response(content=json_str, media_type="application/json")

@app.api_route("/", methods=["GET", "POST"])
async def root_handler(request: Request):
    if request.method == "POST":
        try:
            body = await request.json()
            if "query" in body:
                from app.services.solver import solve_query
                return create_raw_json_response({"output": solve_query(body["query"])})
        except Exception:
            pass
    return create_raw_json_response({"message": "API is running"})

app.include_router(answer_router, prefix="/v1")
