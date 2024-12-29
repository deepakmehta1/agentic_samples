# arithmetic_agent/main.py

from agent.agent import Agent
from agent.memory import MemorySaver
from config.config import SYSTEM_PROMPT


def setup_agent():
    """
    Initializes the agent with tools and memory.
    """
    memory = MemorySaver()
    agent = Agent(SYSTEM_PROMPT, memory)
    return agent


def main():
    agent = setup_agent()
    print(
        "Welcome! You can perform arithmetic operations. Type 'exit' or 'quit' to end the session."
    )
    while True:
        try:
            user_input = input("You: ").strip()
            print("-" * 100)
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            response = agent.interact(user_input)
            print("-" * 100)
            print(f"Assistant: {response}")
            print("-" * 100)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
