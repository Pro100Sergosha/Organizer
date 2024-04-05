# This is function, where user can enter numbers and make math
def main():
    print("Select operation: \n1. Add\n2. Subtract\n3. Multiply\n4. Divide")
    while True:
        choice = input("Enter choice (1/2/3/4): ")
        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print("Result:", add(num1, num2))
            elif choice == '2':
                print("Result:", subtract(num1, num2))
            elif choice == '3':
                print("Result:", multiply(num1, num2))
            elif choice == '4':
                print("Result:", divide(num1, num2))
            break
        else:
            print("Invalid Input")

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

main()
