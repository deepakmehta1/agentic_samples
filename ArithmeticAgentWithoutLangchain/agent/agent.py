import inspect
from openai import OpenAI
import json
from config.config import OPENAI_API_KEY, MODEL_NAME
from .memory import MemorySaver
from tools.tools import (
    get_tools,
    get_tool_schemas,
)  # Import tools and schemas from tools directory


class Agent:
    def __init__(self, tools, memory_saver):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.tools = tools
        self.memory = memory_saver

    def call_llm(self):
        try:
            tool_schemas = (
                get_tool_schemas()
            )  # Get the tool schemas from the tools module

            # Now pass the 'functions' to the API
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=self.memory.get_messages(),
                temperature=0,
                max_tokens=1000,
                n=1,
                stop=None,
                tools=tool_schemas,
            )

            assistant_message = response.choices[0].message.content
            if assistant_message:
                assistant_message = (
                    assistant_message.strip()
                )  # Strip the content only if it's not None
            else:
                assistant_message = "No direct message from the assistant."  # Handle the case when content is None

            self.memory.add_message("assistant", assistant_message)

            # Access tool_calls correctly as a list
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    # Print out tool details
                    print(f"Tool ID: {tool_call.id}")
                    print(f"Tool Name: {tool_call.function.name}")
                    print(f"Arguments: {tool_call.function.arguments}")

                    # Execute the tool based on the name and arguments
                    tool_name = tool_call.function.name

                    # Here we check if the arguments are a string and parse it
                    args_str = (
                        tool_call.function.arguments
                    )  # This is the string like '{"a": 3, "b": 4}'
                    try:
                        args = json.loads(
                            args_str
                        )  # Parse the string into a dictionary
                    except json.JSONDecodeError:
                        args = {}  # Default to empty dictionary if parsing fails
                        print(
                            f"Error parsing arguments for tool {tool_name}: {args_str}"
                        )

                    # Dynamically map arguments using the function's signature
                    if isinstance(args, dict):
                        func = self.tools.get(tool_name)
                        if func:
                            # Get the function signature to match arguments dynamically
                            signature = inspect.signature(func)
                            bound_args = signature.bind(
                                **args
                            )  # Bind arguments from the dictionary to the function's signature
                            bound_args.apply_defaults()  # Ensure default values are applied for missing arguments
                            args = list(
                                bound_args.arguments.values()
                            )  # Convert bound arguments to a list

                    result = self.execute_tool(tool_name, args)
                    print(f"Tool result: {result}")
                    self.memory.add_message("tool", f"Result of {tool_name}: {result}")

            return assistant_message

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None

    def parse_tool_request(self, message):
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

    def execute_tool(self, tool, args):
        func = self.tools.get(tool)
        if func:
            try:
                result = func(*args)
                return result
            except Exception as e:
                return f"Error executing tool '{tool}': {e}"
        return f"Tool '{tool}' not found."

    def interact(self, user_input):
        self.memory.add_message("user", user_input)
        assistant_response = self.call_llm()
        if assistant_response is None:
            return "There was an error processing your request."

        tool, args = self.parse_tool_request(assistant_response)
        if tool:
            print(f"Executing tool: {tool} with arguments {args}")
            result = self.execute_tool(tool, args)
            tool_message = f"Result of {tool}({', '.join(map(str, args))}) is {result}"
            self.memory.add_message("tool", tool_message)
            print(f"Tool result: {result}")
            follow_up = self.call_llm()
            if follow_up:
                print(f"Assistant: {follow_up}")
                return follow_up
            else:
                return "There was an error processing the tool's result."
        else:
            print(f"Assistant: {assistant_response}")
            return assistant_response
