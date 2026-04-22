import json
import re
from typing import List, Optional
from fastapi import FastAPI, Response
from pydantic import BaseModel

# Models
class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

def extract_numbers(text: str) -> List[int]:
    """
    Extracts integers from text. If there's a colon, only looks at the part after it.
    Handles: 'Numbers: 2,5,8,11', 'List: 10, 21, 32', 'From [2, 5, 8, 11]'
    """
    # If colon present, take the part after it
    target = text.split(":", 1)[1] if ":" in text else text
    # Extract from brackets if present
    bracket = re.search(r"\[([^\]]+)\]", target)
    if bracket:
        target = bracket.group(1)
    # Find all integers
    return [int(n) for n in re.findall(r"-?\d+", target) if int(n) < 1000000]

def solve(query: str) -> str:
    q = query.lower().strip()
    nums = extract_numbers(query)

    if not nums:
        return "I could not determine the answer."

    # --- SUM OPERATIONS ---
    if "sum" in q or "total" in q or "add" in q:
        if "even" in q:
            return str(sum(n for n in nums if n % 2 == 0))
        if "odd" in q:
            return str(sum(n for n in nums if n % 2 != 0))
        return str(sum(nums))

    # --- COUNT OPERATIONS ---
    if "count" in q or "how many" in q:
        if "even" in q:
            return str(len([n for n in nums if n % 2 == 0]))
        if "odd" in q:
            return str(len([n for n in nums if n % 2 != 0]))
        return str(len(nums))

    # --- MAX OPERATIONS ---
    if "max" in q or "largest" in q or "greatest" in q or "biggest" in q or "maximum" in q or "highest" in q:
        if "even" in q:
            evens = [n for n in nums if n % 2 == 0]
            return str(max(evens)) if evens else "0"
        if "odd" in q:
            odds = [n for n in nums if n % 2 != 0]
            return str(max(odds)) if odds else "0"
        return str(max(nums))

    # --- MIN OPERATIONS ---
    if "min" in q or "smallest" in q or "least" in q or "lowest" in q or "minimum" in q:
        if "even" in q:
            evens = [n for n in nums if n % 2 == 0]
            return str(min(evens)) if evens else "0"
        if "odd" in q:
            odds = [n for n in nums if n % 2 != 0]
            return str(min(odds)) if odds else "0"
        return str(min(nums))

    # --- AVERAGE ---
    if "average" in q or "mean" in q:
        if "even" in q:
            evens = [n for n in nums if n % 2 == 0]
            if evens:
                avg = sum(evens) / len(evens)
                return str(int(avg)) if avg == int(avg) else str(avg)
        if "odd" in q:
            odds = [n for n in nums if n % 2 != 0]
            if odds:
                avg = sum(odds) / len(odds)
                return str(int(avg)) if avg == int(avg) else str(avg)
        avg = sum(nums) / len(nums)
        return str(int(avg)) if avg == int(avg) else str(avg)

    # --- PRODUCT ---
    if "product" in q or "multiply" in q:
        if "even" in q:
            evens = [n for n in nums if n % 2 == 0]
            result = 1
            for n in evens: result *= n
            return str(result)
        if "odd" in q:
            odds = [n for n in nums if n % 2 != 0]
            result = 1
            for n in odds: result *= n
            return str(result)
        result = 1
        for n in nums: result *= n
        return str(result)

    # Default: return the sum
    return str(sum(nums))


# App
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
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
