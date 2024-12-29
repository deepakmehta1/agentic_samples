# DatabaseAgent/config/config.py

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

def generate_system_prompt(table_schema: str) -> dict:
    """
    Generates the system prompt with the given table schema.

    :param table_schema: The schema of the table to be included in the prompt.
    :return: The system prompt as a dictionary.
    """
    system_prompt_content = f"""
    You run in a loop of Thought, Action, PAUSE, Action_Response.

    At the end of the loop you output an Answer.

    Use Thought to understand the question you have been asked.
    Use Action to break the query down into multiple SQL queries, execute them one by one, and then return PAUSE.
    Action_Response will be the result of executing those SQL queries.

    If necessary, consider the following Table Schema before generating the query:
    {table_schema}

    Example session:

    Question: What is the total sales for the last month?
    Thought: I need to break the query into multiple SQL queries to find the total sales.
    Action: SELECT SUM(sales) FROM transactions WHERE transaction_date BETWEEN '2024-11-01' AND '2024-11-30';
    PAUSE

    You will be called again with this:

    Action_Response: 5000

    You then output:

    Answer: The total sales for the last month is 5000.

    If the result is not final, do not show the result to the user.
    If the result is the final answer to the user's query, set show_to_user to true.
    Use Thought to decide when to respond to the user, and only output final answers when appropriate.

    Your task is to decide when and how to use the tools available to you and when to show the response to the user.
    """

    return {
        "role": "system",
        "content": system_prompt_content
    }

# Example usage:
table_schema_example = """
Table Name: transactions
Columns: transaction_id (INT), transaction_date (DATE), sales (DECIMAL)
"""
system_prompt = generate_system_prompt(table_schema_example)
