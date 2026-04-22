from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.schemas import QueryRequest
from app.services.solver import solve_query

router = APIRouter()

@router.post("/answer")
async def answer_query(request: QueryRequest):
    output = solve_query(request.query)
    # Use explicit JSONResponse to match the root handler's consistency
    return JSONResponse(content={"output": output})
