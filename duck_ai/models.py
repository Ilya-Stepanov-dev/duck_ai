from pydantic import BaseModel

from duck_ai.enums import ModelType, Role


class Message(BaseModel):
    role: Role
    content: str


class Data(BaseModel):
    model: ModelType = ModelType.GPT4o
    messages: list[Message] = []


class HistoryModel(Data):
    vqd: str
