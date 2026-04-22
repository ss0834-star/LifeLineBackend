import sys
from app.services.solver import solve_query

queries = [
    # Level 1
    ("What is 10 + 15?", "The sum is 25."),
    ("Calculate 7 - 2", "The difference is 5."),
    ("9 * 6", "The product is 54."),
    ("20 / 5", "The quotient is 4.0."),
    ("100 / 0", "Division by zero is not allowed."),
    ("What is the sum of 10 and 15?", "The sum is 25."),
    ("difference between 10 and 15", "The difference is -5."),
    
    # Level 2
    ("Convert 2024-03-12 to readable date", "12 March 2024"),
    
    # Level 3
    ("Is 8 even?", "YES"),
    ("Is 7 even?", "NO"),
    
    # Level 4
    ("Numbers: 2,5,8,11. Sum even numbers.", "10"),
    ("Numbers: 1,2,3,4,5. Sum odd numbers.", "9"),
    ("List: 10, 21, 32, 43. Count even values.", "2"),
    ("From [2, 5, 8, 11], total sum.", "26"),
    ("Numbers are 2 5 8 11. Max value.", "11"),
]

for q, expected in queries:
    res = solve_query(q)
    print(f"Q: {q}")
    print(f"Expected: {expected}")
    print(f"Got     : {res}")
    print(f"Pass: {res == expected}\n")
