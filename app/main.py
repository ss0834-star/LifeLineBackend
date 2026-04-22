import json
import re
from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

def solve_math(query: str) -> str:
    # 1. Level 3 Parity check (YES/NO tokens)
    # High priority because it uses specific uppercase tokens
    if "even" in query.lower() or "odd" in query.lower():
        # Avoid picking up Level 4 list operations
        if "numbers" not in query.lower() and ":" not in query:
            num_match = re.search(r"\d+", query)
            if num_match:
                n = int(num_match.group(0))
                is_even = n % 2 == 0
                if "even" in query.lower(): return "YES" if is_even else "NO"
                return "YES" if not is_even else "NO"

    # 2. Level 2 Date formatting (12 March 2024)
    # Handles 2024-03-12, 12-03-2024, or 12/03/2024
    iso_date = re.search(r"(\d{4})-(\d{2})-(\d{2})", query)
    uk_date = re.search(r"(\d{2})[-/](\d{2})[-/](\d{4})", query)
    date_obj = None
    if iso_date:
        date_obj = datetime.strptime(iso_date.group(0), "%Y-%m-%d")
    elif uk_date:
        date_obj = datetime.strptime(uk_date.group(0), "%d-%m-%Y") if "-" in uk_date.group(0) else datetime.strptime(uk_date.group(0), "%d/%m/%Y")
    
    if date_obj:
        # %-d removes leading zero on day. %B is full month name.
        return date_obj.strftime("%-d %B %Y")

    # 3. Level 1 Arithmetic (Sentence style: The sum is 25.)
    # Supports negative numbers and different operators
    arith_match = re.search(r"(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)", query)
    if arith_match:
        a, op, b = arith_match.groups()
        a, b = int(a), int(b)
        if op == "+": return f"The sum is {a + b}."
        if op == "-": return f"The difference is {a - b}."
        if op == "*": return f"The product is {a * b}."
        if op == "/": 
            res = a / b
            return f"The quotient is {float(res)}."

    # 4. Level 4 List aggregate (Bare integer string: 10)
    q = query.lower()
    target = query.split(":", 1)[1] if ":" in query else query
    nums = [int(n) for n in re.findall(r"-?\d+", target)]
    if nums:
        if "sum" in q or "total" in q:
            if "even" in q: return str(sum(n for n in nums if n % 2 == 0))
            if "odd" in q: return str(sum(n for n in nums if n % 2 != 0))
            return str(sum(nums))
        if "count" in q or "how many" in q:
            if "even" in q: return str(len([n for n in nums if n % 2 == 0]))
            if "odd" in q: return str(len([n for n in nums if n % 2 != 0]))
            return str(len(nums))
        if "max" in q or "largest" in q: return str(max(nums))
        if "min" in q or "smallest" in q: return str(min(nums))
        if "average" in q or "mean" in q:
            avg = sum(nums) / len(nums)
            return str(int(avg)) if avg == int(avg) else str(avg)

    return "I could not determine the answer."

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "READY"}

@app.post("/v1/answer")
async def answer(request: QueryRequest):
    result = solve_math(request.query)
    # Character-perfect zero-whitespace JSON output
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
