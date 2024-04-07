import math
import re
# hello world
# This is the main function where the user can enter numbers and perform math operations
def main():
    while True:
        expression = input("Enter an expression: ")

        # Validate input
        if not is_valid_expression(expression):
            print("Invalid expression. Please enter a valid expression.")
            continue

        # Check for square root or square operation
        if 'sqrt' in expression:
            result = calculate_sqrt(expression)
            if result is not None:
                print("Result:", result)
        elif 'square' in expression:
            result = calculate_square(expression)
            if result is not None:
                print("Result:", result)
        else:
            # Split the expression into operands and operator
            operator = get_operator(expression)
            num1, num2 = map(float, expression.split(operator))

            # Perform calculation based on operator
            if operator == '+':
                print("Result:", add(num1, num2))
            elif operator == '-':
                print("Result:", subtract(num1, num2))
            elif operator == '*':
                print("Result:", multiply(num1, num2))
            elif operator == '/':
                print("Result:", divide(num1, num2))
            elif operator == '%':
                print("Result:", percent(num1, num2))

        again = input("Do you want to perform another calculation? (yes/no): ")
        if again.lower() != 'yes':
            break

def is_valid_expression(expression):
    valid_operators = ['+', '-', '*', '/', '%']
    keywords = ['sqrt', 'square']
    
    # Split the expression based on operators and keywords
    parts = re.split(r'(\+|-|\*|/|%|sqrt|square)', expression)
    
    # Iterate over the parts to check validity
    for part in parts:
        part = part.strip()  # Remove leading and trailing whitespace
        if part:  # Check if the part is not empty
            if part not in valid_operators and not part.isdigit() and part not in keywords:  # Check if it's not a valid operator, number, or keyword
                return False
    return True



# This is function to get the operator from the expression
def get_operator(expression):
    for char in expression:
        if char in ['+', '-', '*', '/', '%']:
            return char

# This is function to calculate square root
def calculate_sqrt(expression):
    try:
        num = float(expression.split('sqrt')[1])
        if num < 0:
            return "Error! Square root of a negative number is not allowed."
        return math.sqrt(num)
    except:
        return "Error! Invalid expression for square root."

# This is function to calculate square
def calculate_square(expression):
    try:
        num = float(expression.split('square')[1])
        return num ** 2
    except:
        return "Error! Invalid expression for square."

# This is function for adding numbers
def add(x, y):
    return x + y

# This is function for subtracting numbers
def subtract(x, y):
    return x - y

# This is function for multiplying numbers
def multiply(x, y):
    return x * y

# This is function for dividing numbers
def divide(x, y):
    if y == 0:
        return "Error! Division by zero is not allowed."
    else:
        return x / y

# This is function for %
def percent(x, y):
    a = x * y
    return a / 100

main()
