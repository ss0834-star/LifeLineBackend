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
    q = query.lower()
    
    # 1. Level 3 Parity (YES/NO) - HIGH PRIORITY
    if "is " in q and ("even" in q or "odd" in q) and ":" not in q and "numbers" not in q:
        num_match = re.search(r"\b\d+\b", query)
        if num_match:
            n = int(num_match.group(0))
            is_even = n % 2 == 0
            if "even" in q: return "YES" if is_even else "NO"
            return "YES" if not is_even else "NO"

    # 2. Level 2 Dates (12 March 2024)
    # Support multiple formats and textual input
    date_patterns = [
        r"(\d{4})-(\d{2})-(\d{2})", # ISO
        r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", # UK/US
        r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})" # Textual
    ]
    for pattern in date_patterns:
        match = re.search(pattern, query)
        if match:
            try:
                date_str = match.group(0)
                if "-" in date_str and len(date_str.split("-")[0]) == 4:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                elif "-" in date_str:
                    dt = datetime.strptime(date_str, "%d-%m-%Y")
                elif "/" in date_str:
                    dt = datetime.strptime(date_str, "%d/%m/%Y")
                else:
                    dt = datetime.strptime(date_str, "%d %B %Y")
                return dt.strftime("%-d %B %Y")
            except: continue

    # 3. Level 1 Arithmetic (Sentences)
    # Check for text like "sum of 10 and 15" or "10 + 15"
    arith_match = re.search(r"(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)", query)
    if arith_match:
        a, op, b = arith_match.groups()
        a, b = int(a), int(b)
        if op == "+": return f"The sum is {a + b}."
        if op == "-": return f"The difference is {a - b}."
        if op == "*": return f"The product is {a * b}."
        if op == "/": return f"The quotient is {float(a / b)}."

    # 4. Level 4 Lists (Integers) - BROAD SUPPORT
    # Isolate list data after colon or inside brackets
    target = query.split(":", 1)[1] if ":" in query else query
    bracket = re.search(r"\[(.*?)\]", target)
    if bracket: target = bracket.group(1)
    
    nums = [int(n) for n in re.findall(r"-?\d+", target)]
    if nums:
        if "sum" in q or "total" in q or "add" in q:
            if "even" in q: return str(sum(n for n in nums if n % 2 == 0))
            if "odd" in q: return str(sum(n for n in nums if n % 2 != 0))
            return str(sum(nums))
        if "count" in q or "how many" in q:
            if "even" in q: return str(len([n for n in nums if n % 2 == 0]))
            if "odd" in q: return str(len([n for n in nums if n % 2 != 0]))
            return str(len(nums))
        if "max" in q or "largest" in q or "biggest" in q or "highest" in q: return str(max(nums))
        if "min" in q or "smallest" in q or "lowest" in q: return str(min(nums))
        if "average" in q or "mean" in q:
            avg = sum(nums) / len(nums)
            return str(int(avg)) if avg == int(avg) else str(avg)

    return "I could not determine the answer."

app = FastAPI()

@app.get("/")
async def root():
    return Response(
        content=json.dumps({"status": "VERSION_95_PERCENT_ULTIMATE"}, separators=(',', ':')),
        media_type="application/json"
    )

@app.post("/v1/answer")
async def answer(request: QueryRequest):
    result = solve_math(request.query)
    # Character-perfect zero-whitespace JSON
    return Response(
        content=json.dumps({"output": result}, separators=(',', ':')),
        media_type="application/json"
    )
