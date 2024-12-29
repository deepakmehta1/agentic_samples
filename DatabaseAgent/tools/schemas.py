# tools/schemas.py

sql_query_executer_schema = {
    "type": "function",
    "function": {
        "name": "sql_query_executer",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}
