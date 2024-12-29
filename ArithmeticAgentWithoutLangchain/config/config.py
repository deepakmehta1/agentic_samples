# arithmetic_agent/config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. Please set it in the .env file."
    )

# Model configuration
MODEL_NAME = "gpt-4o-2024-08-06"  # Ensure you have access to this model

# Memory configuration
MEMORY_FILEPATH = "memory.json"

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You run in a loop of Thought, Action, PAUSE, Action_Response.\n\n"
        "At the end of the loop you output an Answer.\n\n"
        "Use Thought to understand the question you have been asked.\n"
        "Use Action to run one of the actions available to you — then return PAUSE.\n"
        "Action_Response will be the result of running those actions.\n\n"
        "Your available actions are:\n\n"
        "add: e.g. add(2, 4)\n"
        "Returns the sum of two numbers.\n\n"
        "subtract: e.g. subtract(5, 3)\n"
        "Returns the result of subtracting the second number from the first.\n\n"
        "multiply: e.g. multiply(2, 3)\n"
        "Returns the product of two numbers.\n\n"
        "divide: e.g. divide(6, 3)\n"
        "Returns the quotient of dividing the first number by the second.\n\n"
        "Example session:\n\n"
        "Question: What is 2 + 4?\n"
        "Thought: I should perform the addition of 2 and 4.\n"
        'Action: {"function_name": "add", "function_parms": {"a": 2, "b": 4}}\n'
        "PAUSE\n\n"
        "You will be called again with this:\n\n"
        "Action_Response: 6\n\n"
        "You then output:\n\n"
        "Answer: The result of 2 + 4 is 6.\n\n"
        "If the result is not final, do not show the result to the user.\n"
        "If the result is the final answer to the user's query, set show_to_user to true.\n"
        "Use Thought to decide when to respond to the user, and only output final answers when appropriate.\n\n"
        "Your task is to decide when and how to use the tools available to you and when to show the response to the user."
    ),
}
