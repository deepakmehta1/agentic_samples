# arithmetic_agent/agent/memory.py

import json
import os
from config.config import MEMORY_FILEPATH, SYSTEM_PROMPT


class MemorySaver:
    def __init__(self, filepath=MEMORY_FILEPATH):
        self.filepath = filepath
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    self.messages = json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Warning: {self.filepath} is corrupted. Initializing with system prompt."
                )
                self.messages = [SYSTEM_PROMPT]
        else:
            self.messages = [SYSTEM_PROMPT]

    def save(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.messages, f, indent=2)
        except Exception as e:
            print(f"Error saving memory to {self.filepath}: {e}")

    def add_message(self, role, content, name=None):
        if role == "function":
            self.messages.append({"role": role, "content": content, "name": name})
        else:
            self.messages.append({"role": role, "content": content})
        self.save()

    def get_messages(self):
        return self.messages

    def clear_memory(self):
        self.messages = []
        self.save()
