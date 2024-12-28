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
MODEL_NAME = "gpt-4"  # Ensure you have access to this model

# Memory configuration
MEMORY_FILEPATH = "memory.json"

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful assistant tasked with performing arithmetic on a set of inputs. "
        "When you need to perform an arithmetic operation, respond with a JSON object specifying the tool and its arguments. "
        'For example: {"tool": "add", "args": [5, 3]}'
    ),
}
