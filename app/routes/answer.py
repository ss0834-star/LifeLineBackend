from fastapi import APIRouter
from app.models.schemas import QueryRequest
from app.services.solver import solve_query

router = APIRouter()

@router.post("/answer")
def answer_query(request: QueryRequest):
    output = solve_query(request.query)
    # Manual dictionary return to avoid any Pydantic model serialization overhead/extra fields
    return {"output": output}
