from fastapi import FastAPI
from app.routes.answer import router as answer_router

app = FastAPI(title="API Evaluation Platform Backend")

@app.get("/")
def health_check():
    return {"message": "API is running"}

app.include_router(answer_router, prefix="/v1")
