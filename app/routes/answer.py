from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.schemas import QueryRequest
from app.services.solver import solve_query

router = APIRouter()

@router.post("/answer")
async def answer_query(request: QueryRequest):
    """
    Evaluator endpoint. 
    Strictly follows the JSON response contract: {"output": "..."}
    """
    result = solve_query(request.query)
    
    # JSONResponse with compact separators to ensure minimal hidden variations
    return JSONResponse(
        content={"output": result},
        headers={"Content-Type": "application/json"}
    )
