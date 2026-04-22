import re
from typing import Tuple, Optional

def extract_expression(text: str) -> Optional[Tuple[int, str, int]]:
    """
    Extracts an arithmetic expression (a + b, a - b, a * b, a / b) from natural language text.
    """
    pattern = r"(-?\d+)\s*([\+\-\*\/])\s*(-?\d+)"
    match = re.search(pattern, text)
    if match:
        op1, operator, op2 = match.groups()
        return int(op1), operator, int(op2)
    return None

def extract_date(text: str) -> Optional[str]:
    """
    Extracts a date like '12 March 2024' or 'March 12, 2024' from text.
    """
    date_pattern = r"(\d{1,2}\s+[A-Za-z]+\s+\d{4})"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)
    return None

def extract_parity_query(text: str) -> Optional[int]:
    """
    Extracts the number from queries like 'Is 9 an odd number?' or 'Is 10 even?'.
    """
    # Regex to find a number followed by or preceded by even/odd keywords
    # Example: "Is 9 an odd number?"
    pattern = r"(\d+)"
    match = re.search(pattern, text)
    if match and ("odd" in text.lower() or "even" in text.lower()):
        return int(match.group(1))
    return None
