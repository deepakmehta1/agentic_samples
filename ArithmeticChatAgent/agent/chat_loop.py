from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


def chat_loop(agent_graph):
    """
    Starts the interactive chat loop with the user.
    """
    print("Welcome to ArithmeticChatAgent! Type 'exit' to quit.\n")
    thread_id = "1"  # Default thread ID for simplicity

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Create a HumanMessage from user input
        messages = [HumanMessage(content=user_input)]

        # Configuration with thread ID for memory
        config = {"configurable": {"thread_id": thread_id}}

        # Invoke the agent graph with the messages and configuration
        response = agent_graph.invoke({"messages": messages}, config)

        # Process and display each message in the response
        for msg in response["messages"]:
            if isinstance(msg, AIMessage):
                print(f"AI: {msg.content}\n")
            elif isinstance(msg, HumanMessage):
                print(f"You: {msg.content}\n")
            elif isinstance(msg, SystemMessage):
                print(f"System: {msg.content}\n")
            else:
                # Handle Tool Messages
                if hasattr(msg, "name") and hasattr(msg, "output"):
                    print(f"Tool ({msg.name}): {msg.output}\n")
