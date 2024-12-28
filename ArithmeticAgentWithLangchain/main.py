from utils.environment import load_environment
from agent.agent_setup import setup_agent
from agent.chat_loop import chat_loop


def main():
    """
    Main function to run the ArithmeticChatAgent application.
    """
    # Load environment variables
    load_environment()

    # Setup the agent
    agent_graph = setup_agent()

    # Start the chat loop
    chat_loop(agent_graph)


if __name__ == "__main__":
    main()
