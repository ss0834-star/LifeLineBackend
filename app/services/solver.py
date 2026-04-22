from app.utils import parser

def solve_query(query: str) -> str:
    """
    Hybrid rule-based solver.
    Priority is meticulously ordered to prevent cross-level interference.
    """
    normalized = parser.normalize_query(query)

    # 1. Level 4: List / Aggregate Operations
    list_op = parser.detect_list_operation(query)
    if list_op:
        target_text = query
        if ":" in query:
            target_text = query.split(":", 1)[1]
        
        nums = parser.extract_numbers_from_text(target_text)
        if nums:
            res = 0
            if list_op == "sum_even":
                res = sum(n for n in nums if n % 2 == 0)
            elif list_op == "sum_odd":
                res = sum(n for n in nums if n % 2 != 0)
            elif list_op == "count_even":
                res = len([n for n in nums if n % 2 == 0])
            elif list_op == "count_odd":
                res = len([n for n in nums if n % 2 != 0])
            elif list_op == "sum_all":
                res = sum(nums)
            elif list_op == "max":
                res = max(nums)
            elif list_op == "min":
                res = min(nums)
            elif list_op == "average":
                res = sum(nums) / len(nums)
            
            # FORMATTING FIX: Return purely as an integer string if it's a whole number.
            # This ensures "10" instead of "10.0" for sum/count/max/min.
            if res == int(res):
                return str(int(res))
            return str(res)

    # 2. Level 2: Date Formatting
    if parser.detect_date_formatting_request(query):
        date_obj = parser.extract_date_candidate(query)
        if date_obj:
            return date_obj.strftime("%d %B %Y").lstrip("0")

    # 3. Level 3: Parity Tokens (YES/NO)
    parity_num = parser.detect_parity_request(query)
    if parity_num is not None:
        is_even = parity_num % 2 == 0
        if "even" in normalized:
            return "YES" if is_even else "NO"
        if "odd" in normalized:
            return "YES" if not is_even else "NO"

    # 4. Level 1: Basic Arithmetic
    arith = parser.extract_arithmetic_expression(query)
    if arith:
        op1, op, op2 = arith
        try:
            if op == '+':
                res = op1 + op2
                val = int(res) if res == int(res) else res
                return f"The sum is {val}."
            if op == '-':
                res = op1 - op2
                val = int(res) if res == int(res) else res
                return f"The difference is {val}."
            if op == '*':
                res = op1 * op2
                val = int(res) if res == int(res) else res
                return f"The product is {val}."
            if op == '/':
                if op2 == 0:
                    return "Division by zero is not allowed."
                res = op1 / op2
                return f"The quotient is {float(res)}."
        except Exception:
            pass

    return "I could not determine the answer."
