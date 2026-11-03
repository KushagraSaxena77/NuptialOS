import asyncio

from langchain.messages import HumanMessage
from agents.coordinator import build_coordinator


async def main():
    print("Starting Wedding Planner Agent.")

    agent = await build_coordinator()

    config = {"configurable": {"thread_id": "WeddingPlanner-1"}}

    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        user_query = input("Give wedding details please: ")

        if user_query in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = await agent.ainvoke({"messages": [HumanMessage(content=user_query)]}, config=config)
        final_response = response["messages"][-1].text

        print("\nWedding Plan\n")
        print(final_response)

if __name__ == "__main__":
    asyncio.run(main())

#I am in London, I want to have a wedding in Paris. Guest count would be 200 people and I want jazz genre of music in my wedding.My boarding date should be 12-11-2026 and return date should be 17-11-2026

