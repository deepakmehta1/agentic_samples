# tools/tools.py

from tools.functions import add, subtract, multiply, divide
from tools.schemas import add_schema, subtract_schema, multiply_schema, divide_schema

# Tools dictionary mapping function names to actual functions
TOOLS = {"add": add, "subtract": subtract, "multiply": multiply, "divide": divide}

# List of tool schemas
TOOL_SCHEMAS = [add_schema, subtract_schema, multiply_schema, divide_schema]


# Functions to access tools and schemas
def get_tool_schemas():
    return TOOL_SCHEMAS


def get_tools():
    return TOOLS
