import json
import re
from types import TracebackType
from typing import Self
import aiohttp
from .models import ModelType, Data , Message, Role

type json_str = str

URL = 'https://duckduckgo.com/duckchat/v1/'

class AiChat:
    def __init__(self,
        model: ModelType = ModelType.GPT4o,
        messages: list[Message] | None = None,
        session: aiohttp.ClientSession | None = None,
        vqd: str = '1'
        ) -> None:
        self._session = session or aiohttp.ClientSession()
        self.vqd = vqd 

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
            headers = {'x-vqd-accept': self.vqd},
        ) as response:
            
            if response.status != 200:
                raise Exception(f"Failed to initialize chat: {response.status} {await response.text()}")
            if "x-vqd-4" in response.headers:
                self.vqd = response.headers["x-vqd-4"]


    async def send_request(self, message: str) ->str :
        self.data.messages.append(Message(role=Role.user, content=message))

        if self.vqd == '1':
            await self._get_vqd()
        
        async with self._session.post(
            url = URL + 'chat', 
            headers = {
                "x-vqd-4": self.vqd,
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            }, 
            data=self.data.model_dump_json(),
        ) as response:     
                   
            if response.status != 200:
                raise Exception(f"Failed to send message: {response.status} {await response.text()}")
            self.vqd = response.headers["x-vqd-4"]

            response = await response.text()
            response = self._glue_response(response)
            self.data.messages.append(Message(role=Role.assistant, content=response))
            return response
