# arithmetic_agent/agent/tools.py


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a / b


# Dictionary of available tools
TOOLS = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}
