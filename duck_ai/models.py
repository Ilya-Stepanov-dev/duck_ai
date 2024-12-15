from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    USER = 'user'
    ASSISTANT = 'assistant'


class ModelType(str, Enum):
    GPT4o = "gpt-4o-mini"
    Claude = "claude-3-haiku-20240307"
    Llama = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    Mixtral = "mistralai/Mixtral-8x7B-Instruct-v0.1"


class Message(BaseModel):
    role: Role
    content: str


class Data(BaseModel):
    model: ModelType = ModelType.GPT4o
    messages: list[Message] = []


class HistoryModel(Data):
    vqd: str