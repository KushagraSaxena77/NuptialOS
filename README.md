# NuptialOS

NuptialOS is a multi agent wedding planning assistant built with LangChain and LangGraph. It combines specialist agents for travel, venues and music to produce a structured wedding plan from natural language requirements.

The application is designed to preserve wedding details across a conversation, delegate each planning task to the appropriate specialist and combine the returned information through a central coordinator.

Example Usage: 

> I am in London, I want to have a wedding in Paris. Guest count would be 200 people and I want jazz genre of music in my wedding.My
 boarding date should be 12-11-2026 and return date should be 17-11-2026.


You may trace your agent thinking in LangSmith, similar like this.


<img width="1509" height="786" alt="image" src="https://github.com/user-attachments/assets/0521dabd-b4d3-414f-9a02-df7ea0655761" />

---

## Features

1. Extracts the wedding origin, destination, guest count, music genre and travel dates from a user request.
2. Preserves the extracted details through LangGraph state.
3. Searches for return flights through the Kiwi MCP service.
4. Researches wedding venues through Tavily web search.
5. Retrieves music recommendations from the included Chinook SQLite database.
6. Coordinates specialist results into one wedding plan.
7. Supports follow up questions through an in memory conversation checkpoint.
---
## Architecture

The application uses a coordinator and three specialist agents.

1. **Coordinator agent**
   Extracts requirements, updates state and calls relevant specialists.
2. **Travel specialist**
   Searches for flights through the Kiwi MCP service.
3. **Venue specialist**
   Searches the web for suitable wedding venues.
4. **Music specialist**
   Retrieves tracks by genre from the Chinook database.
5. **Wedding state**
   Stores the planning details shared across the conversation.
6. **Wedding tools**
   Exposes state updates and specialist calls to the coordinator.

The main workflow is:

1. The user provides wedding requirements.
2. The coordinator extracts the available details.
3. The coordinator stores the details in the wedding state.
4. Relevant specialist agents run their searches.
5. The coordinator combines the specialist results into a final plan.
---
## Requirements

1. Python 3.13 or a compatible later version.
2. uv for Python environment and dependency management.
3. Ollama with the model configured in `config.py`.
4. A Tavily API key for venue research.
5. Network access to the Kiwi MCP service for flight searches.
---
## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/KushagraSaxena77/NuptialOS.git
cd NuptialOS
```

Install the project dependencies:

```bash
uv sync
```

Create the environment file:

```bash
cp .env.example .env
```

Set the required values in `.env`, especially `TAVILY_API_KEY`. The other provider and LangSmith values are optional unless the related services are being used.

Start Ollama and download the model named in `config.py` using the corresponding Ollama command:

```bash
ollama serve
```
> [!TIP]
> You may use any AI LLM of your choice, just configure your API Key in .env file and change your model in config.py.

## Running the application

Run the interactive planner with:

```bash
uv run python main.py
```

Enter wedding requirements when prompted. Use `exit` or `quit` to end the session.

Example request:

```text
I am in London and want to have a wedding in Paris for 200 guests. I would like jazz music. My travel dates are 12 11 2026 to 17 11 2026.
```

The coordinator expects travel dates in day, month, year order. It stores them as `DD MM YYYY` values for the flight specialist.
---
## Configuration

Configuration is loaded from `.env` through `python dotenv`.

1. **`TAVILY_API_KEY`**
   Enables venue and related web research.
2. **`LANGSMITH_API_KEY`**
   Enables LangSmith integration.
3. **`LANGSMITH_TRACING`**
   Controls LangSmith tracing.
4. **`LANGSMITH_ENDPOINT`**
   LangSmith service endpoint.
5. **`LANGSMITH_PROJECT`**
   LangSmith project name.

The language model, temperature and context size are configured in `config.py`.
---
## Data sources and integrations

### Kiwi MCP

The travel specialist connects to `https://mcp.kiwi.com` through the LangChain MCP adapter. Flight information is only reported when it is returned by the flight search service.

### Tavily

The venue specialist uses Tavily to research venues based on destination and guest count. Results depend on the information returned by the web search service.

### Chinook

Music recommendations use `resources/Chinook.db`. The playlist tool joins the `Track`, `Genre`, `Album` and `Artist` tables and returns up to 20 tracks for the requested genre.

## Project structure

```text
NuptialOS
    agents
        coordinator.py
        specialists.py
    resources
        Chinook.db
    tools
        playlist_db.py
        web_search.py
        wedding_tools.py
    config.py
    langgraph.json
    main.py
    pyproject.toml
    state.py
```
---
## LangGraph development server

The graph is registered in `langgraph.json` under the name `wedding_planner`. To use the LangGraph command line interface, run:

```bash
uv run langgraph dev
```

This starts the configured graph using the local project environment.

<img width="727" height="796" alt="image" src="https://github.com/user-attachments/assets/4d0fdffb-cd20-4664-a7e5-165629a078ca" />

## Development notes

1. The coordinator updates state before calling specialist tools.
2. Specialist tools should not invent flight, venue or database information.
3. Flight dates are interpreted in day, month, year order.
4. The current checkpoint uses in memory storage, so state is not retained after the process stops.
5. The current command line interface is intended for local interactive use.

---
## Author

Kushagra Saxena
