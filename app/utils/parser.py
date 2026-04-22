import re
from datetime import datetime
from typing import Tuple, Optional, List

def normalize_query(text: str) -> str:
    """Lowercases and strips basic noise for intent detection."""
    return text.lower().strip()

def extract_arithmetic_expression(text: str) -> Optional[Tuple[float, str, float]]:
    """
    Robustly extracts arithmetic patterns. 
    Handles: 10 + 15, Calculate 7 - 2, 9 * 6, 20 / 5, -4 + 9.
    """
    # Regex targets num op num.
    # Handles negatives and decimals.
    pattern = r"(-?\d+\.?\d*)\s*([\+\-\*\/])\s*(-?\d+\.?\d*)"
    match = re.search(pattern, text)
    if match:
        op1, operator, op2 = match.groups()
        return float(op1), operator, float(op2)
    return None

def extract_numbers_from_text(text: str) -> List[float]:
    """Extracts all numbers from text, including those in lists/brackets."""
    # Matches integers and decimals
    return [float(n) for n in re.findall(r"-?\d+\.?\d*", text)]

def detect_list_operation(text: str) -> Optional[str]:
    """Detects list intents: sum, count, max, min, average."""
    t = text.lower()
    if "average" in t: return "average"
    if "sum" in t or "total" in t or "add" in t:
        if "even" in t: return "sum_even"
        if "odd" in t: return "sum_odd"
        return "sum_all"
    if "count" in t or "how many" in t:
        if "even" in t: return "count_even"
        if "odd" in t: return "count_odd"
        return "count_all"
    if "max" in t or "largest" in t or "biggest" in t or "highest" in t: return "max"
    if "min" in t or "smallest" in t or "lowest" in t: return "min"
    return None

def detect_parity_request(text: str) -> Optional[float]:
    """Detects if query is a direct parity check: 'Is 8 even?'."""
    t = text.lower()
    if "even" in t or "odd" in t:
        nums = extract_numbers_from_text(text)
        if len(nums) == 1 and ("is" in t or "?" in t or "check" in t or "tell" in t):
            return nums[0]
    return None

def extract_date_candidate(text: str) -> Optional[datetime]:
    """
    Attempts to parse a date from various formats.
    Matches: 2024-03-12, 12/03/2024, 2024/03/12, 12 March 2024.
    """
    # Try ISO-like YYYY-MM-DD or YYYY/MM/DD
    iso_match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", text)
    if iso_match:
        try:
            return datetime(int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3)))
        except ValueError: pass

    # Try DD/MM/YYYY or DD-MM-YYYY
    uk_match = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", text)
    if uk_match:
        try:
            # Assume DD/MM/YYYY
            return datetime(int(uk_match.group(3)), int(uk_match.group(2)), int(uk_match.group(1)))
        except ValueError: pass

    # Try DD Month YYYY
    word_match = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
    if word_match:
        try:
            return datetime.strptime(f"{word_match.group(1)} {word_match.group(2)} {word_match.group(3)}", "%d %B %Y")
        except ValueError:
            try:
                return datetime.strptime(f"{word_match.group(1)} {word_match.group(2)} {word_match.group(3)}", "%d %b %Y")
            except ValueError: pass

    return None

def detect_date_formatting_request(text: str) -> bool:
    """Detects if the intent is to reformat or convert a date."""
    t = text.lower()
    keywords = ["convert", "reformat", "format", "change", "into", "readable", "natural"]
    return any(k in t for k in keywords) and extract_date_candidate(text) is not None
