import json
import re
from typing import List, Optional
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

# 1. Models
class QueryRequest(BaseModel):
    query: str
    assets: Optional[List[str]] = []

# 2. Solver Logic (Integrated for maximum speed and simplicity)
def extract_numbers(text: str) -> List[int]:
    """Extracts all integers from the text part after the colon."""
    target = text.split(":", 1)[1] if ":" in text else text
    return [int(n) for n in re.findall(r"\d+", target)]

def solve(query: str) -> str:
    nums = extract_numbers(query)
    q = query.lower()
    
    if not nums:
        return "I could not determine the answer."
        
    # Priority 1: Sum Even
    if "sum" in q and "even" in q:
        return str(sum(n for n in nums if n % 2 == 0))
    
    # Priority 2: Sum Odd
    if "sum" in q and "odd" in q:
        return str(sum(n for n in nums if n % 2 != 0))
    
    # Priority 3: Max
    if "max" in q or "largest" in q:
        return str(max(nums))
    
    # Priority 4: Total Sum
    if "sum" in q:
        return str(sum(nums))
        
    return str(nums[0])

# 3. App
app = FastAPI()

@app.api_route("/", methods=["GET", "POST"])
async def root():
    return {"message": "API is running"}

@app.post("/v1/answer")
async def answer(request: QueryRequest):
    result = solve(request.query)
    # Character-perfect JSON with NO spaces
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
