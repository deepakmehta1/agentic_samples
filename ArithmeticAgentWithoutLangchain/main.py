# arithmetic_agent/main.py

from agent.agent import Agent
from agent.memory import MemorySaver
from agent.tools import TOOLS


def setup_agent():
    """
    Initializes the agent with tools and memory.
    """
    memory = MemorySaver()
    agent = Agent(TOOLS, memory)
    return agent


def main():
    agent = setup_agent()
    print(
        "Welcome! You can perform arithmetic operations. Type 'exit' or 'quit' to end the session."
    )
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            response = agent.interact(user_input)
            print(f"Assistant: {response}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
