from app.utils.parser import extract_expression

def solve_query(query: str) -> str:
    """
    Parses the query and returns the exact answer string based on the operator.
    """
    parsed = extract_expression(query)
    if not parsed:
        return "I could not determine the answer."
    
    op1, operator, op2 = parsed
    
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
        return f"The quotient is {ans}."
    
    return "I could not determine the answer."
