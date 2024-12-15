import asyncio

from duck_ai.api import AiChat
from duck_ai.history.json_history import JsonHistory

async def main():
    history = JsonHistory(path_file='.storage/data2.json')

    async with AiChat(history=history) as chat:
        while True:
            user_input = input("You: \n")
            response = await chat.send_request(user_input)
            print(f'Assistant: \n{response}')

if __name__ == "__main__":
    asyncio.run(main())