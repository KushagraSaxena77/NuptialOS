from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from config import get_model
from state import WeddingState
from agents.specialists import build_SpecialistAgent  
from tools.wedding_tools import build_weddingTools

async def build_coordinator():

    model = get_model()

    travel_agent, venue_agent, playlist_agent = await build_SpecialistAgent()

    wedding_tools = build_weddingTools(travel_agent= travel_agent, venue_agent=venue_agent, playlist_agent=playlist_agent)

    main_agent = create_agent(
        model = model,
        tools= wedding_tools,
        state_schema= WeddingState,
        system_prompt='''
        You are the Coordinator Agent for a wedding planning assistant.

        You have four tools:

        1. update_state
        2. flight_search
        3. venue_search
        4. suggest_playlist

        Follow this workflow:

        STEP 1: EXTRACT INFORMATION

        Extract the following details from the user's messages:
        - Origin
        - Wedding destination
        - Guest count
        - Music genre

        STEP 2: UPDATE STATE

        If the required details are available, call update_state.

        Call update_state alone.
        Do not call any other tool in the same response.

        STEP 3: SPECIALIST EXECUTION

        After update_state succeeds:

        Identify all relevant specialist tools.

        Call all relevant specialist tools together in parallel.
        Do not wait for one specialist before calling another.

        STEP 4: FINAL RESPONSE

        Wait for the specialist results.

        Combine their findings into one wedding plan.

        Rules:
        - Never invent prices, availability, venues, flights or database records.
        - Do not assume missing travel dates or budgets.
        - Explain when additional information is required.
        - Do not call irrelevant tools.
        - Do not repeat specialist searches unnecessarily.
        - Use British English.
        - Do not use emojis or unnecessary formatting.
        - Be clear and concise.
        - When the user provides travel dates, extract them in DD-MM-YYYY format.
            Save them using:
            - boarding_date
            - return_date

        When the user provides additional information in a follow up message,
        preserve previously saved wedding details.

        Do not ask the user to confirm dates that they have already explicitly provided.

        STRICT RESULT VALIDATION:

        - Only use flight information returned by the travel specialist.
        - Never generate airline names, flight times, airports or prices yourself.
        - If the travel specialist did not call a flight search tool,
        report that flight search was unsuccessful.
        - Give links to flight in response using flight_search tool which is using kiwi mcp.
        - Never describe flights as available or confirmed without
        actual tool results.
        ''',
        checkpointer= InMemorySaver()
    ) 

    return main_agent