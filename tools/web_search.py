from tavily import TavilyClient
from langchain.tools import tool

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> str:
    """Search the web for wedding venues and related information."""
    return tavily_client.search(query)