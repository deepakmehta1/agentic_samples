# model/response.py

from pydantic import BaseModel


class OpenAIResponse(BaseModel):
    content: (
        str  # The content of the response, which can be a message from the assistant.
    )
    show_to_user: (
        bool  # A boolean that decides whether the content should be shown to the user.
    )
