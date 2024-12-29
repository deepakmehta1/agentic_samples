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


class Agent:
    def __init__(self, system_prompt, memory_saver, tools=get_tools()):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.system_prompt = system_prompt
        self.memory = memory_saver
        self.tools = tools

    def __get_messages(self):
        return [self.system_prompt] + (self.memory.get_messages())

    def call_llm(self):
        try:
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

            assistant_message = response.choices[0].message.parsed
            message_type = "assistant"

            # Access tool_calls correctly as a list
            tool_calls = response.choices[0].message.tool_calls
            if tool_calls:
                message_type = "tools"  # If there are tool calls, it's a tool message
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
                    result_string = f"Tool result: {result}"
                    # self.memory.add_message("tool", f"Result of {tool_name}: {result}")

                    # Send the result back to the model if it's a tool call
                    # You can store it in memory or process the next steps
                    # tool_event = {
                    #     'tool': result,
                    #     'status': 'completed'
                    # }
                    self.memory.add_message(
                        "function", result_string, tool_call.function.name
                    )
                    # self.memory.add_message("user", 'multiply 3 by 4')
            return assistant_message, message_type

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None, None  # Return None if error occurs

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

        while True:
            assistant_response, message_type = self.call_llm()

            if message_type == "tools":
                # If it's a tool call, process it and send the result back to the model
                print(f"Processing tool call: {assistant_response}")
                # Store the tool result in memory (this is optional, based on your design)
            else:
                # If it's the assistant's final response, we show it to the user
                print(f"internal processing: {assistant_response}")
                self.memory.add_message("assistant", assistant_response.content)
                if assistant_response.show_to_user:
                    return assistant_response.content
