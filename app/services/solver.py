from app.utils import parser

def solve_query(query: str) -> str:
    """
    Dedicated solver for Level 4.
    Extracts numbers and performs the requested list operation.
    Guarantees strict string integer output for whole numbers.
    """
    # Force Level 4 logic as the primary and only priority
    # This identifies: sum even, sum odd, count, max, min, average
    list_op = parser.detect_list_operation(query, parser.extract_numbers_from_text(query))
    
    # We isolate the numbers specifically from the data part of the string
    target_text = query
    if ":" in query:
        target_text = query.split(":", 1)[1]
    
    nums = parser.extract_numbers_from_text(target_text)
    
    if nums:
        res = 0
        # If the query asks for "sum even numbers", result is 10 for [2, 5, 8, 11]
        if list_op == "sum_even":
            res = sum(n for n in nums if n % 2 == 0)
        elif list_op == "sum_odd":
            res = sum(n for n in nums if n % 2 != 0)
        elif list_op == "count_even":
            res = len([n for n in nums if n % 2 == 0])
        elif list_op == "count_odd":
            res = len([n for n in nums if n % 2 != 0])
        elif list_op == "sum_all" or not list_op:
            # Default to total sum if no specific operation is detected
            res = sum(nums)
        elif list_op == "max":
            res = max(nums)
        elif list_op == "min":
            res = min(nums)
        elif list_op == "average":
            res = sum(nums) / len(nums) if len(nums) > 0 else 0
        
        # STRICT FORMATTING: Return exactly "10" for a result of 10.0
        if res == int(res):
            return str(int(res))
        return str(res)

    # Fallback for non-numeric queries
    return "I could not determine the answer."
