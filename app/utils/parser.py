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
    Specifically targets the Level 2 requirement.
    """
    # Regex to match: Day(1-2 digits) Month(Word) Year(4 digits)
    # Example: "12 March 2024"
    date_pattern = r"(\d{1,2}\s+[A-Za-z]+\s+\d{4})"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)
    return None
