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
MODEL_NAME = "gpt-4o"  # Ensure you have access to this model

# Memory configuration
MEMORY_FILEPATH = "memory.json"

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful assistant. You can use the available tools to perform arithmetic operations when necessary. "
        "Please provide clear, natural language responses to the user's queries. "
        "If a calculation is needed, use the appropriate tool and respond with the result in a conversational manner. "
        "Do not return any JSON objects in your replies."
    ),
}
