# tools/schemas.py

sql_query_executer_schema = {
    "type": "function",
    "function": {
        "name": "sql_query_executer",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}
