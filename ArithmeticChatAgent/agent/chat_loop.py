# agent/chat_loop.py

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import json


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
                # Handle Tool Invocation Messages
                if (
                    hasattr(msg, "additional_kwargs")
                    and "tool_calls" in msg.additional_kwargs
                ):
                    tool_calls = msg.additional_kwargs["tool_calls"]
                    for tool_call in tool_calls:
                        tool_name = tool_call.get("function", {}).get(
                            "name", "Unknown Tool"
                        )
                        tool_args_json = tool_call.get("function", {}).get(
                            "arguments", "{}"
                        )
                        try:
                            tool_args = json.loads(tool_args_json)
                        except json.JSONDecodeError:
                            tool_args = (
                                tool_args_json  # Keep as string if JSON parsing fails
                            )
                        print(f"Tool Called: {tool_name}")
                        print(f"Arguments: {tool_args}\n")

                # Handle Tool Response Messages
                elif hasattr(msg, "name") and hasattr(msg, "content"):
                    tool_name = msg.name
                    tool_output = msg.content
                    print(f"Tool ({tool_name}) Output: {tool_output}\n")

                # Handle Other Messages (if any)
                else:
                    print(f"Unknown message type: {msg}\n")
