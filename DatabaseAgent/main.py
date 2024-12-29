# tools/main.py

from agent.agent import Agent
from agent.memory import MemorySaver
from config.config import system_prompt
from db_connector.connector import DBConnector
from typing import NoReturn


def setup_agent() -> Agent:
    """
    Initializes the agent with tools, memory, and database connection.

    Returns:
        Agent: An instance of the Agent class with initialized memory, tools, and DB connection.
    """
    memory = MemorySaver()  # Initialize memory
    db_connector = DBConnector()  # Initialize DBConnector
    db_connector.connect()  # Establish the database connection
    agent = Agent(
        system_prompt, memory, db_connector
    )  # Initialize agent with system prompt, memory, and DB connection
    return agent


def main() -> NoReturn:
    """
    Starts the main interaction loop with the user. The loop handles user inputs and interacts with the assistant.
    """
    agent = setup_agent()
    print("Welcome! Search for flights. Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            user_input = input("You: ").strip()  # Get user input
            print("-" * 100)

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break  # Exit the loop if user types 'exit' or 'quit'

            response = agent.interact(user_input)  # Get the assistant's response
            print("-" * 100)
            print(f"Assistant: {response}")
            print("-" * 100)

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break  # Exit gracefully on KeyboardInterrupt or EOFError


if __name__ == "__main__":
    main()
