# tools/schemas.py

add_schema = {
    "type": "function",
    "function": {
        "name": "add",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        },
    },
}

subtract_schema = {
    "type": "function",
    "function": {
        "name": "subtract",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        },
    },
}

multiply_schema = {
    "type": "function",
    "function": {
        "name": "multiply",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        },
    },
}

divide_schema = {
    "type": "function",
    "function": {
        "name": "divide",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        },
    },
}
