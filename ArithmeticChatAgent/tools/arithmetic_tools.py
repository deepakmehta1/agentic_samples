# tools/arithmetic_tools.py

def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies two integers."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divides two integers."""
    if b == 0:
        return float('inf')  # Handle division by zero
    return a / b

# List of available tools
TOOLS = [add, multiply, divide]
