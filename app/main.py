import json
import re
from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []


def solve(query: str) -> str:
    # Step 1: Extract the numbers from the query
    # e.g. "Numbers: 2,5,8,11. Sum even numbers." -> [2, 5, 8, 11]
    target = query.split(":", 1)[1] if ":" in query else query
    nums = [int(n) for n in re.findall(r"-?\d+", target)]

    if not nums:
        return "0"

    # Step 2: Sum only the even numbers and return as plain integer string
    return str(sum(n for n in nums if n % 2 == 0))


app = FastAPI()


@app.get("/")
async def root():
    return Response(
        content=json.dumps({"message": "API is running"}, separators=(',', ':')),
        media_type="application/json"
    )


@app.post("/v1/answer")
async def answer(request: QueryRequest):
    result = solve(request.query)
    # Strict JSON: {"output":"10"} with zero whitespace
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
