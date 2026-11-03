from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command


def build_weddingTools(travel_agent, venue_agent, playlist_agent):

    @tool
    async def flight_search(runtime: ToolRuntime) -> str:
        """Find flights using the saved origin and destination."""
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]
        boarding_date = runtime.state["boarding_date"]
        return_date = runtime.state["return_date"]
    
        if not origin or not destination:
            return "Flight search unavailable: origin or destination is missing."


        response = await travel_agent.ainvoke({"messages":[HumanMessage(content=f"Find one way or return economy flights from {origin} to {destination} on {boarding_date} and {return_date}")]})

        
        return response["messages"][-1].text

    @tool
    async def venue_search(runtime: ToolRuntime) -> str:
        '''Venue agent chooses the best venue for the given location and capacity.'''
        destination = runtime.state["destination"]
        guest_count = runtime.state["guest_count"]


        if not destination or guest_count is None:
            return "Venue search unavailable: destination or guest count is missing."

        
        response = await venue_agent.ainvoke({"messages": [HumanMessage(content=f"Find venue in {destination} for {guest_count} guests")]})

        return response["messages"][-1].text

    @tool
    async def suggest_playlist(runtime: ToolRuntime) -> str:
        '''Playlist agent curates the perfect playlist for the given genre.'''

        genre = runtime.state["genre"]
 
        response = await playlist_agent.ainvoke({"messages":[HumanMessage(content= f"Find {genre} tracks for wedding playlist")]})

        return response["messages"][-1].text

    @tool
    def update_state(origin: str, destination: str, guest_count: int, genre: str, boarding_date: str, return_date: str, runtime: ToolRuntime) -> Command:
        """Update the state when you know all of the values: origin, destination, guest_count, genre, boarding_date, return_date. 
            This tool must be called alone, without any other tool calls. It must complete and return to make,
            the information available to other tools."""

        if guest_count < 1:
            raise ValueError("Guest count must be at least 1.")

        return Command(
            update={
                "origin":origin,
                "destination": destination,
                "guest_count": guest_count,
                "genre": genre,
                "boarding_date": boarding_date,
                "return_date": return_date,
                "messages": [ToolMessage(content= "Successfully updated state", tool_call_id = runtime.tool_call_id)],
            }
            )

    return [update_state, flight_search, venue_search, suggest_playlist]
    
    
