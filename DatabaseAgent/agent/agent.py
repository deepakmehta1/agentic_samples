import inspect
from openai import OpenAI
import json
from config.config import OPENAI_API_KEY, MODEL_NAME
from .openai_response import OpenAIResponse
from .memory import MemorySaver
from tools.tools import (
    get_tools,
    get_tool_schemas,
)
from db_connector.connector import DBConnector
from typing import List, Tuple, Optional, Dict


class Agent:
    def __init__(
        self,
        system_prompt: dict,
        memory_saver: MemorySaver,
        db_connector: DBConnector,
        tools: Dict[str, callable] = get_tools(),
    ) -> None:
        """
        Initializes the Agent class with the system prompt, memory, and available tools.

        Args:
            system_prompt: The initial prompt to guide the assistant's responses.
            memory_saver: Memory object to handle message storage.
            tools: A dictionary of available tools for the assistant.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.system_prompt = system_prompt
        self.memory = memory_saver
        self.tools = tools
        self.db_connector = db_connector

    def __get_messages(self) -> List[dict]:
        """
        Retrieves the list of messages from the system prompt and memory.

        Returns:
            List of messages to send to the LLM (Large Language Model).
        """
        return [self.system_prompt] + self.memory.get_messages()

    def call_llm(self) -> Tuple[Optional[str], str]:
        """
        Calls the LLM (Large Language Model) API and processes the response.

        Returns:
            - assistant_message: The assistant's message content or None.
            - message_type: The type of message ('tools' or 'assistant').
        """
        try:
            # Send request to LLM with messages and tools
            response = self.client.beta.chat.completions.parse(
                model=MODEL_NAME,
                messages=self.__get_messages(),
                temperature=0,
                max_tokens=1000,
                n=1,
                stop=None,
                tools=get_tool_schemas(),
                response_format=OpenAIResponse,
            )

            assistant_message = response.choices[
                0
            ].message.content  # Correct access to message content
            message_type = "assistant"  # Default to assistant response

            if assistant_message:
                assistant_message = (
                    assistant_message.strip()
                )  # Strip content to remove leading/trailing whitespace
            else:
                assistant_message = "No direct message from the assistant."  # Default if no message content

            # Access tool_calls correctly if any exist
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                message_type = "tools"  # If there are tool calls, it's a tool message
                for tool_call in tool_calls:
                    # Print tool call details for debugging
                    print(f"Tool ID: {tool_call.id}")
                    print(f"Tool Name: {tool_call.function.name}")
                    print(f"Arguments: {tool_call.function.arguments}")

                    # Process tool call arguments
                    tool_name = tool_call.function.name
                    args_str = (
                        tool_call.function.arguments
                    )  # String representing tool arguments
                    try:
                        args = json.loads(
                            args_str
                        )  # Parse the arguments string into a dictionary
                    except json.JSONDecodeError:
                        args = {}  # Default to empty dictionary if parsing fails
                        print(
                            f"Error parsing arguments for tool {tool_name}: {args_str}"
                        )

                    # Dynamically map arguments to the function's signature
                    if isinstance(args, dict):
                        func = self.tools.get(tool_name)
                        if func:
                            signature = inspect.signature(
                                func
                            )  # Get the function signature
                            bound_args = signature.bind(
                                **args
                            )  # Bind arguments to the function signature
                            bound_args.apply_defaults()  # Apply default values for missing arguments
                            args = list(
                                bound_args.arguments.values()
                            )  # Convert to a list for function call

                    # Execute the tool based on the mapped arguments
                    result = self.execute_tool(tool_name, args)
                    print(f"Tool result: {result}")
                    result_string = f"Tool result: {result}"

                    # Send the tool result back to the model if it is a tool call
                    self.memory.add_message(
                        "function", result_string, tool_call.function.name
                    )

            return (
                assistant_message,
                message_type,
            )  # Return both assistant message and message type

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None, None  # Return None if an error occurs

    def parse_tool_request(
        self, message: str
    ) -> Tuple[Optional[str], Optional[List[dict]]]:
        """
        Parses the assistant's message to detect if it involves a tool request.

        Args:
            message: The assistant's message to parse.

        Returns:
            - tool: The tool to be invoked (e.g., 'add', 'subtract').
            - args: A list of arguments for the tool, or None if no tool is found.
        """
        try:
            json_start = message.find("{")
            json_end = message.rfind("}") + 1
            if json_start == -1 or json_end == 0:
                return None, None
            json_str = message[json_start:json_end]
            data = json.loads(json_str)
            tool = data.get("tool")
            args = data.get("args", [])
            if tool in self.tools and isinstance(args, list):
                return tool, args
        except (json.JSONDecodeError, AttributeError):
            pass
        return None, None

    def execute_tool(self, tool: str, args: List) -> str:
        """
        Executes the tool based on the provided name and arguments.

        Args:
            tool: The tool's name to execute (e.g., 'add', 'multiply').
            args: The arguments for the tool.

        Returns:
            - result: The result of executing the tool as a string.
        """
        func = self.tools.get(tool)
        if func:
            try:
                result = func(*args)
                return result
            except Exception as e:
                return f"Error executing tool '{tool}': {e}"
        return f"Tool '{tool}' not found."

    def interact(self, user_input: str) -> str:
        """
        Processes the user's input, interacts with the assistant, and manages tool calls.

        Args:
            user_input: The input message from the user.

        Returns:
            - The final assistant message or tool result.
        """
        self.memory.add_message("user", user_input)

        while True:
            assistant_response, message_type = self.call_llm()  # Call the LLM

            if assistant_response is None:
                return "There was an error processing your request."

            if message_type == "tools":
                # If it's a tool call, process it and send the result back to the model
                print(f"Processing tool call: {assistant_response}")
                # Store the tool result in memory (this is optional)
            else:
                # If it's the assistant's final response, return it to the user
                print(f"Internal processing: {assistant_response}")
                self.memory.add_message("assistant", assistant_response)
                if (
                    assistant_response.show_to_user
                ):  # Only return the result if show_to_user is True
                    return assistant_response.content
