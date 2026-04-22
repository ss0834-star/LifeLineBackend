from app.utils.parser import extract_expression, extract_date

def solve_query(query: str) -> str:
    """
    Parses the query and returns the exact answer string required by the evaluator.
    Supports Level 1 (Arithmetic) and Level 2 (Date Extraction).
    """
    # Try Level 2: Date Extraction
    date_match = extract_date(query)
    if date_match:
        # Based on screenshot, expected output is just the date string: "12 March 2024"
        return date_match

    # Try Level 1: Arithmetic
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
