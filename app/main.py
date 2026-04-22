from fastapi import FastAPI
from app.routes.answer import router as answer_router

app = FastAPI(title="API Evaluation Platform Backend")

# Redirect root POST requests to v1/answer if they contain a query
# This acts as a fallback for some evaluators that hit the root with a POST
@app.post("/")
async def root_post_redirect(request: dict):
    if "query" in request:
        from app.services.solver import solve_query
        return {"output": solve_query(request["query"])}
    return {"message": "API is running"}

@app.get("/")
def health_check():
    return {"message": "API is running"}

app.include_router(answer_router, prefix="/v1")
