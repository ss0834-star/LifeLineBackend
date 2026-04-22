from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.solver import solve_query

router = APIRouter()

@router.post("/answer", response_model=QueryResponse)
def answer_query(request: QueryRequest):
    output = solve_query(request.query)
    return QueryResponse(output=output)
