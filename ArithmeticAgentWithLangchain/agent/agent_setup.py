from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from tools.arithmetic_tools import TOOLS


def setup_agent():
    """
    Initializes the language model with tools and configures the agent with memory.
    """
    # Initialize the language model
    llm = ChatOpenAI(model="gpt-4o")
    llm_with_tools = llm.bind_tools(TOOLS)

    # System message to define the assistant's role
    sys_msg = SystemMessage(
        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
    )

    # Define the assistant node
    def assistant(state: MessagesState):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    # Build the state graph
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")

    # Initialize memory saver for persistence
    memory = MemorySaver()
    react_graph_memory = builder.compile(checkpointer=memory)

    return react_graph_memory
