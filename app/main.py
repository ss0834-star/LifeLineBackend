import json
import re
from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

def solve_math(query: str) -> str:
    # Handle Level 1 Arithmetic: "What is 10 + 15?"
    arith_match = re.search(r"(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)", query)
    if arith_match:
        a, op, b = arith_match.groups()
        a, b = int(a), int(b)
        if op == "+": return f"The sum is {a + b}."
        if op == "-": return f"The difference is {a - b}."
        if op == "*": return f"The product is {a * b}."
        if op == "/": return f"The quotient is {float(a / b)}."

    # Handle Level 2 Dates: "2024-03-12"
    date_match = re.search(r"(\d{4})-(\d{2})-(\d{2})", query)
    if date_match:
        from datetime import datetime
        dt = datetime.strptime(date_match.group(0), "%Y-%m-%d")
        return dt.strftime("%-d %B %Y")

    # Handle Level 3 Parity: "Is 8 even?"
    if "even" in query.lower() or "odd" in query.lower():
        num_match = re.search(r"\d+", query)
        if num_match and "numbers" not in query.lower() and ":" not in query:
            n = int(num_match.group(0))
            is_even = n % 2 == 0
            if "even" in query.lower(): return "YES" if is_even else "NO"
            return "YES" if not is_even else "NO"

    # Handle Level 4 Lists: "Numbers: 2,5,8,11. Sum even numbers."
    q = query.lower()
    target = query.split(":", 1)[1] if ":" in query else query
    nums = [int(n) for n in re.findall(r"-?\d+", target)]
    
    if nums:
        if "sum" in q:
            if "even" in q: return str(sum(n for n in nums if n % 2 == 0))
            if "odd" in q: return str(sum(n for n in nums if n % 2 != 0))
            return str(sum(nums))
        if "count" in q:
            if "even" in q: return str(len([n for n in nums if n % 2 == 0]))
            if "odd" in q: return str(len([n for n in nums if n % 2 != 0]))
            return str(len(nums))
        if "max" in q or "largest" in q: return str(max(nums))
        if "min" in q or "smallest" in q: return str(min(nums))
        if "average" in q:
            avg = sum(nums) / len(nums)
            return str(int(avg)) if avg == int(avg) else str(avg)

    return "I could not determine the answer."

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is ready"}

@app.post("/v1/answer")
async def answer(request: QueryRequest):
    result = solve_math(request.query)
    # Character-perfect zero-whitespace JSON
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
