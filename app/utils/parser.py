import re
from typing import Tuple, Optional

def extract_expression(text: str) -> Optional[Tuple[int, str, int]]:
    """
    Extracts an arithmetic expression (a + b, a - b, a * b, a / b) from natural language text.
    Supports basic natural language math questions.
    """
    # Pattern to find numbers and operators even with some words around them
    # Example: "What is 10 + 15?" -> finds 10, +, 15
    pattern = r"(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)"
    
    match = re.search(pattern, text)
    if match:
        op1, operator, op2 = match.groups()
        return int(op1), operator, int(op2)
    
    return None
