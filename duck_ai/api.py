import json
import re
from types import TracebackType
from typing import Self
import aiohttp
from .models import Message, Role
from .history.history import History
from .history.json_history import JsonHistory


type json_str = str

URL = 'https://duckduckgo.com/duckchat/v1/'

# TODO Придумать, что сделать с save_storage()

class AiChat:
    def __init__(self,
                session: aiohttp.ClientSession | None = None,
                history: History | None = None
        ) -> None:

        self._session = session or aiohttp.ClientSession()
        self.history = history

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
            headers = {'x-vqd-accept': self.history.data.vqd},

        ) as response:
            
            if response.status != 200:
                raise Exception(f"Failed to initialize chat: {response.status} {await response.text()}")
            if "x-vqd-4" in response.headers:
                self.history.data.vqd = response.headers["x-vqd-4"]
                self.history.save_storage()


    async def send_request(self, message: str) -> str:
        self.history.add_message(Message(role=Role.USER, content=message))

        if self.history.data.vqd == '1':
            await self._get_vqd()
        
        async with self._session.post(
            url = URL + 'chat', 
            headers = {
                "x-vqd-4": self.history.data.vqd,
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            }, 
            data=self.history.get_data_json(),
        ) as response:     
                   
            if response.status != 200:
                raise Exception(f"Failed to send message: {response.status} {await response.text()}")
            self.history.data.vqd = response.headers["x-vqd-4"]

            response = await response.text()
            response = self._glue_response(response)
            self.history.add_message(Message(role=Role.ASSISTANT, content=response))
            return response
