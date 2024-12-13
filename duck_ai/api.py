import json
import re
from types import TracebackType
from typing import Self
import aiohttp
from .models import ModelType, Data , Message

type json_str = str

# TODO stream для вывода

URL = 'https://duckduckgo.com/duckchat/v1/'

class AiChat:
    def __init__(self,
        model: ModelType = ModelType.GPT4o,
        messages: list[Message] | None = None,
        session: aiohttp.ClientSession | None = None,
        ) -> None:
        self._session = session or aiohttp.ClientSession()
        self.vqd: str = self._get_vqd()

        if not messages:
            self.data = Data(model=model, messages=[])
        else:
            self.data = Data(model=model, messages=messages)


    async def __aenter__(self) -> Self:
        return self
    

    async def __aexit__ (self, 
                         exc_type: type[BaseException], 
                         exc_value: BaseException, 
                         traceback: TracebackType
            ) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)

    
    def _glue_response(self, response: str):
        pattern = r'data: ({.*?})'
        matches = re.findall(pattern, response)
        messages = []

        for match in matches:
            try:
                data = json.loads(match)
                if 'message' in data:
                    messages.append(data['message'])
            except json.JSONDecodeError:
                continue

        messages = ''.join(messages)
        return messages


    async def _get_vqd(self) -> None:
        async with self._session.get(
            url = URL+'status',
            headers = {'x-vqd-accept:': self.vqd},
        ) as response:
            
            if response.status != 200:
                raise Exception(f"Failed to initialize chat: {response.status} {await response.text()}")
            if "x-vqd-4" in response.headers:
                self.vqd = response.headers["x-vqd-4"]


    async def send_request(self, message: Message) ->str :
        self.data.messages.append(message)
        async with self.session.post(
            url = URL + 'chat', 
            headers = {
                "x-vqd-4": self.vqd,
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            }, 
            data=self.data.messages.model_dump_json(),
        ) as response:
            
            if response.status != 200:
                raise Exception(f"Failed to send message: {response.status} {await response.text()}")
            response = await response.text()
            response = self._glue_response(response)
            self.data.messages.append(response)
            return response 
