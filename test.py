import asyncio
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from config import get_model

async def main():
    model = get_model()

    response = await model.ainvoke([
        HumanMessage(content="Reply with just: Hello")
    ])

    print(response.text)

asyncio.run(main())