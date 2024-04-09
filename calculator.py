import math
import re
from styles import Styles
# This is the main function where the user can enter numbers and perform math operations

class Calculator:
    def __init__(self, style_menu = Styles()):
        self.style_menu = style_menu

    def is_valid_expression(self, expression):
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
    def get_operator(self,expression):
        for char in expression:
            if char in ['+', '-', '*', '/', '%']:
                return char

    # This is function to calculate square root
    def calculate_sqrt(self,expression):
        try:
            num = float(expression.split('sqrt')[1])
            if num < 0:
                return "Error! Square root of a negative number is not allowed."
            return math.sqrt(num)
        except:
            return "Error! Invalid expression for square root."

    # This is function to calculate square
    def calculate_square(self,expression):
        try:
            num = float(expression.split('square')[1])
            return num ** 2
        except:
            return "Error! Invalid expression for square."

    # This is function for adding numbers
    def add(self,x, y):
        return x + y

    # This is function for subtracting numbers
    def subtract(self,x, y):
        return x - y

    # This is function for multiplying numbers
    def multiply(self,x, y):
        return x * y

    # This is function for dividing numbers
    def divide(self,x, y):
        if y == 0:
            return "Error! Division by zero is not allowed."
        else:
            return x / y

    # This is function for %
    def percent(self,x, y):
        a = x * y
        return a / 100

    def calculator_app_menu(self):
        while True:
            expression = input("Enter an expression: ")

            # Validate input
            if not self.is_valid_expression(expression):
                self.style_menu.new_print("Invalid expression. Please enter a valid expression.")
                continue

            # Check for square root or square operation
            if 'sqrt' in expression:
                result = self.calculate_sqrt(expression)
                if result is not None:
                    self.style_menu.new_print(f"Result: srqt {expression} = {result}")
            elif 'square' in expression:
                result = self.calculate_square(expression)
                if result is not None:
                    self.style_menu.new_print(f"Result: square {expression} = {result}")
            else:
                # Split the expression into operands and operator
                operator = self.get_operator(expression)
                num1, num2 = map(float, expression.split(operator))

                # Perform calculation based on operator
                if operator == '+':
                    self.style_menu.new_print(f"Result: {num1} + {num2} = {self.add(num1, num2)}")
                elif operator == '-':
                    self.style_menu.new_print(f"Result: {num1} - {num2} = {self.subtract(num1, num2)}")
                elif operator == '*':
                    self.style_menu.new_print(f"Result: {num1} * {num2} = {self.multiply(num1, num2)}")
                elif operator == '/':
                    self.style_menu.new_print(f"Result: {num1} / {num2} = {self.divide(num1, num2)}")
                elif operator == '%':
                    self.style_menu.new_print(f"Result: {num1} % {num2} = {self.percent(num1, num2)}")

            again = input("Do you want to perform another calculation? (yes/no): ")
            if again.lower() != 'yes':
                return
