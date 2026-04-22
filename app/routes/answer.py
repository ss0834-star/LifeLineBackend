import json
from fastapi import APIRouter, Response
from app.models.schemas import QueryRequest
from app.services.solver import solve_query

router = APIRouter()

@router.post("/answer")
async def answer_query(request: QueryRequest):
    """
    Evaluator endpoint with strict character-perfect output control.
    """
    output = solve_query(request.query)
    
    # Manual serialization to ensure exactly zero extra spaces in the JSON.
    # Output will be: {"output":"10"}
    json_str = json.dumps({"output": output}, separators=(',', ':'))
    return Response(content=json_str, media_type="application/json")
