import json
import os
from config.config import MEMORY_FILEPATH, SYSTEM_PROMPT
from typing import List, Dict, Optional


class MemorySaver:
    def __init__(self, filepath: str = MEMORY_FILEPATH) -> None:
        """
        Initializes the MemorySaver class with a filepath to store messages.

        Args:
            filepath: The file path where messages are saved.
        """
        self.filepath: str = filepath
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    self.messages: List[Dict[str, str]] = json.load(
                        f
                    )  # Load existing messages
            except json.JSONDecodeError:
                print(
                    f"Warning: {self.filepath} is corrupted. Initializing with system prompt."
                )
                self.messages = [SYSTEM_PROMPT]
        else:
            self.messages: List[Dict[str, str]] = [SYSTEM_PROMPT]

    def save(self) -> None:
        """
        Saves the current messages to the memory file.
        """
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.messages, f, indent=2)
        except Exception as e:
            print(f"Error saving memory to {self.filepath}: {e}")

    def add_message(self, role: str, content: str, name: Optional[str] = None) -> None:
        """
        Adds a new message to memory.

        Args:
            role: The role of the message sender (e.g., "user", "assistant", "function").
            content: The content of the message.
            name: Optional name for the function (only used for function role).
        """
        if role == "function":
            self.messages.append({"role": role, "content": content, "name": name})
        else:
            self.messages.append({"role": role, "content": content})
        self.save()

    def get_messages(self) -> List[Dict[str, str]]:
        """
        Retrieves all messages stored in memory.

        Returns:
            A list of dictionaries containing role and content of the messages.
        """
        return self.messages

    def clear_memory(self) -> None:
        """
        Clears all messages from memory.
        """
        self.messages = []
        self.save()
