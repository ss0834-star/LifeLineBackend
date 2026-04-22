from app.utils.parser import extract_expression, extract_date, extract_parity_query

def solve_query(query: str) -> str:
    """
    Parses the query and returns the exact answer string required by the evaluator.
    Supports Level 1 (Math), Level 2 (Date), and Level 3 (Odd/Even).
    """
    q_lower = query.lower()

    # Level 3: Parity (Odd/Even)
    parity_num = extract_parity_query(query)
    if parity_num is not None:
        is_odd_query = "odd" in q_lower
        is_even_query = "even" in q_lower
        
        is_actually_odd = parity_num % 2 != 0
        
        if is_odd_query:
            return "YES" if is_actually_odd else "NO"
        elif is_even_query:
            return "YES" if not is_actually_odd else "NO"

    # Level 2: Date Extraction
    date_match = extract_date(query)
    if date_match:
        return date_match

    # Level 1: Arithmetic
    parsed = extract_expression(query)
    if parsed:
        op1, operator, op2 = parsed
        try:
            if operator == '+':
                ans = op1 + op2
                return f"The sum is {ans}."
            elif operator == '-':
                ans = op1 - op2
                return f"The difference is {ans}."
            elif operator == '*':
                ans = op1 * op2
                return f"The product is {ans}."
            elif operator == '/':
                if op2 == 0:
                    return "Division by zero is not allowed."
                ans = op1 / op2
                if ans == int(ans):
                    return f"The quotient is {float(ans)}."
                return f"The quotient is {ans}."
        except Exception:
            pass

    return "I could not determine the answer."
