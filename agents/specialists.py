from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from config import get_model
from tools.web_search import web_search
from tools.playlist_db import playlist_db

async def build_SpecialistAgent():

    model = get_model()


    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com",
            }
        }
    )

    flight_tools = await client.get_tools()


    travel_agent = create_agent(
        model = model,
        tools= flight_tools,
        system_prompt= '''
        You are a Flight Search Specialist.

        Your job is to search for flights using the available Kiwi MCP tools.

        Instructions:

        1. Always use the available flight search tools when the user
        requests flight availability or prices.

        2. Extract these details:
        - Departure location
        - Arrival location
        - Outbound date
        - Return date
        - Number of passengers, if provided

        3. Interpret dates in DD-MM-YYYY format.
        For example, 12-11-2026 means 12 November 2026.

        4. If the user provides an outbound and return date,
        search for a return journey.

        5. Do not ask for confirmation when all required
        search information is already available.

        6. Never invent flight details, airlines, prices or availability.

        7. If a tool returns an error, report the actual error.

        8. If no suitable tool exists, clearly explain that.

        Never claim that flights are available unless the
        flight search tool returns actual results.

        Use British English.
        Do not use emojis.
        '''
    )


    venue_agent = create_agent(
        model= model,
        tools= [web_search],
        system_prompt= '''
             You are a Wedding Venue Specialist.
             
             Your task is to find venues that match the user's requirements.
             
                Focus on:
                - Wedding destination and location
                - Guest capacity
                - Budget, when provided
                - Venue type and preferences
                - Relevant facilities and services
             
                Rules:
                - Use the available tools to research venues when appropriate.
                - Do not invent venue names, prices, guest capacities, or facilities.
                - Distinguish verified information from information that is unavailable.
                - If key requirements are missing, ask for clarification when necessary.
                - Present the most relevant results in a clear, organised format.
                - If no suitable results are found, state that honestly.
               
            '''
        )


    playlist_agent = create_agent(
        model = model,
        tools = [playlist_db],
        system_prompt= '''
        You are a Wedding Music Specialist.

        Your job is to recommend music based on the user's preferences.

        Instructions:
        - Use the playlist_db tool to retrieve songs.
        - The database is Chinook.
        - It uses Track, Genre, Album and Artist tables.
        - There is no Songs table.
        - Use Genre.Name to filter music genres.
        - Use Track.Name for song titles.
        - Use Artist.Name for artist names.
        - Never invent database records.
        - You may provide additional recommendations, but clearly
        distinguish them from database results.
        - Organise recommendations by wedding event when useful.
        - Use British English.
        - Do not use emojis.
        '''
    )

    return travel_agent, venue_agent, playlist_agent