from langchain.agents import AgentState

class WeddingState(AgentState, total=False): #total=False allows these fields to be absent initially, before the coordinator has extracted and saved the wedding details.
    origin: str
    destination: str
    guest_count: int
    genre: str
    boarding_date: str
    return_date: str
 


