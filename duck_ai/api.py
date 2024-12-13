import json
import re
from typing import Self
import aiohttp
from .models import ModelType, History , Message

# TODO прописать генератор для сессий

HEADERS_SESSION = {
    "Host": "duckduckgo.com",
    # "Accept": "text/event-stream",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Referer": "https://duckduckgo.com/",
    # "User-Agent": self.user_agent,
    # "DNT": "1",
    # "Sec-GPC": "1",
    # "Connection": "keep-alive",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    # "TE": "trailers",
}

type json_str = str

class Request:
    def __init__(self, 
                 url: str, 
                 header: dict, 
                 data: json_str = ''
        ) -> None:

        self.url = url
        self.header = header
        self.data = data

    # def get(self) -> dict:
    #     return {self.url.__name__ : self.url,
    #             self.header.__name__ : self.header,
    #     }

    # def post(self) -> dict:
    #     return vars(self)

class AiChat:
    def __init__(self,
        model: ModelType = ModelType.GPT4o,
        history: list[Message] | None = None,
        session: aiohttp.ClientSession | None = None,
        ) -> None:
        self.model = model
        self._session = session or aiohttp.ClientSession(headers=HEADERS_SESSION.copy())
        self.vqd: str = ''

        if not history:
            self.history = History(model=model, history=[])
        else:
            self.history = History(model=model, history=history)

    async def __aenter__(self) -> Self:
        return self
    
    async def __aexit__ (self, ) -> None:
        pass