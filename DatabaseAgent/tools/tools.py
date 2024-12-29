# tools/tools.py

from tools.functions import sql_query_executer
from tools.schemas import sql_query_executer_schema

# Tools dictionary mapping function names to actual functions
TOOLS = {"sql_query_executor": sql_query_executer}

# List of tool schemas
TOOL_SCHEMAS = [sql_query_executer_schema]


# Functions to access tools and schemas
def get_tool_schemas():
    return TOOL_SCHEMAS


def get_tools():
    return TOOLS
