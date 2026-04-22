from app.utils.parser import extract_expression

def solve_query(query: str) -> str:
    """
    Parses the query and returns the exact answer string required by the evaluator.
    Strictly follows: 'The sum/difference/product/quotient is X.'
    """
    parsed = extract_expression(query)
    if not parsed:
        return "I could not determine the answer."
    
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
            # Force .0 for whole number divisions to satisfy '4.0' requirements
            if ans == int(ans):
                return f"The quotient is {float(ans)}."
            return f"The quotient is {ans}."
    except Exception:
        return "I could not determine the answer."
    
    return "I could not determine the answer."
