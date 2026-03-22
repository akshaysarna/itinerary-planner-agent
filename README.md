# Itinerary Planner Agent

An intelligent AI-powered travel planning assistant built with LangChain and Claude that helps users plan trips by automatically finding airports and hotels based on their destination.

## 📋 Project Overview

The Itinerary Planner Agent is a conversational AI system that leverages Claude LLM to provide structured travel itineraries. It uses a multi-tool approach to gather real-time data about airports and hotels, then synthesizes this information into a comprehensive travel plan.

## 🏗️ Architecture

### Project Structure
```
itinerary-planner-agent/
├── main.py                          # Entry point - initializes the agent and logging
├── requirements.txt                 # Python dependencies
├── agents/
│   └── itinerary_agent.py          # Core agent logic with LLM orchestration
├── llm/
│   └── claude.py                   # Claude LLM configuration and initialization
├── services/
│   ├── google_map_service.py       # Google Maps Places API integration
│   └── search_api.py               # External Search API for airport data
└── tools/
    ├── airport_tool.py             # Tool to search nearby airports
    └── hotel_tool.py               # Tool to search available hotels
```

## 🔧 Core Components

### 1. **main.py** - Application Entry Point
- Loads environment variables from `.env` file
- Sets up logging framework (logs to `app.log`)
- Initializes the async itinerary agent
- Entry point for the application

### 2. **agents/itinerary_agent.py** - Agent Orchestration
The core intelligence engine that:
- **Initializes Claude LLM** with haiku-4-5 model
- **Creates tools array** with airport and hotel search tools
- **Defines system prompt** that instructs the AI to:
  1. Identify the destination
  2. Search for nearest airports
  3. Find suitable hotels
  4. Generate a structured itinerary

**Key Features:**
- Conversation memory (last 5 exchanges)
- Tool calling mechanism to perform searches
- Streaming responses for real-time output
- Strict completion rules to prevent redundant API calls
- Structured output format (Destination, Airport, Hotels, Day-wise Itinerary)

### 3. **llm/claude.py** - LLM Configuration
- Wraps Anthropic's Claude API
- Default model: `claude-haiku-4-5`
- Configurable temperature (0.7), streaming, and timeout
- Returns a ChatAnthropic instance for use in agents

### 4. **services/google_map_service.py** - Google Maps Integration
- Calls Google Places API for location searches
- Supports flexible field masking for data retrieval
- Returns place details including:
  - Display name
  - Address
  - Geographic coordinates
  - Ratings (for hotels)
  - Opening hours

**API Configuration via environment variables:**
- `GOOGLE_MAP_PLACE_API_URL` - Base API endpoint
- `GOOGLE_API_TOKEN` - Authentication token

### 5. **services/search_api.py** - Airport Search Service
- Integrates with external airport search API
- `get_airport_details()` - Fetches airport information by city name
- Returns airport codes, names, and location details
- Error handling for API failures

**API Configuration via environment variables:**
- `SEARCH_API_BASE_URL` - Base URL for search service
- `SEARCH_API_KEY` - API authentication key
- `SEARCH_API_AIRPORT_DETAILS` - Endpoint path for airport search

### 6. **tools/airport_tool.py** - Airport Search Tool
**Purpose:** Find airports serving a destination

**Functionality:**
- Takes city name as input
- Queries Google Places API for nearby airports
- Retrieves airport codes from Search API
- Returns: airport name, address, coordinates, airport code
- Limits results to 1-3 most relevant airports

**Tool Usage Rules:**
- Call at most once per request
- Avoid duplicate calls with same input

### 7. **tools/hotel_tool.py** - Hotel Search Tool
**Purpose:** Discover accommodations in a destination

**Functionality:**
- Takes city/location name as input
- Queries Google Places API for hotels
- Returns: hotel name, address, coordinates, ratings
- Sorts results by rating (highest first)
- Filters hotels with rating ≥ 3.5
- Limits results to 5-10 hotels

**Tool Usage Rules:**
- Avoid calling multiple times for same location
- Use results to make informed accommodation decisions

## 📦 Dependencies

```
langchain==1.2.13                  # LLM orchestration framework
langchain-core==1.2.20             # Core LangChain utilities
langchain-anthropic==1.4.0         # Anthropic Claude integration
langchain-community==0.4.1         # Community integrations
python-dotenv>=1.0.0               # Environment variable management
Flask==3.1.3                       # Web framework (optional)
numpy==2.4.3                       # Numerical computing
requests>=2.31.0                   # HTTP library for API calls
```

## 🚀 Usage

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with required environment variables:
   ```
   GOOGLE_MAP_PLACE_API_URL=<Your Google Places API endpoint>
   GOOGLE_API_TOKEN=<Your Google API key>
   SEARCH_API_BASE_URL=<Your Search API base URL>
   SEARCH_API_AIRPORT_DETAILS=<Airport details endpoint>
   SEARCH_API_KEY=<Your Search API key>
   ANTHROPIC_API_KEY=<Your Anthropic API key>
   ```

### Running the Agent
```bash
python main.py
```

### Interaction Flow
1. Start the application
2. Enter your travel query (e.g., "Plan a 3-day trip to Goa")
3. The agent will:
   - Identify the destination
   - Automatically search for nearby airports
   - Find recommended hotels
   - Generate a structured itinerary
4. Enter `0` to exit

### Example Conversation
```
Welcome to Itinerary Portal
> Plan a weekend trip to Mumbai

Destination: Mumbai
Nearest Airport: Bombay International Airport (BOM)
Recommended Hotels (prefer rating):
  1. The Oberoi Mumbai (Rating: 4.6)
  2. Taj Holel (Rating: 4.5)
  3. Hilton Mumbai (Rating: 4.4)
Itinerary:
  1. Day 1: Arrive at BOM, check-in, visit Gateway of India
  2. Day 2: Explore Marine Drive, Bollywood studios
  3. Day 3: Visit markets, depart
```

## 🔄 Workflow

```
User Input
    ↓
[Itinerary Agent]
    ↓
Parse destination
    ↓
Call [Airport Tool] → Google Maps API + Search API
    ↓
Call [Hotel Tool] → Google Maps API
    ↓
Claude LLM synthesizes data
    ↓
Generate structured itinerary
    ↓
Stream response to user
    ↓
Back to user input
```

## 🛠️ Key Features

✅ **AI-Powered Planning** - Uses Claude LLM for intelligent recommendations
✅ **Real-time Data** - Integrates live data from Google Maps and airport APIs
✅ **Asynchronous Processing** - Non-blocking operations for responsive UX
✅ **Conversation Memory** - Maintains context across multiple exchanges
✅ **Structured Output** - Consistent, formatted itinerary responses
✅ **Error Handling** - Comprehensive logging and exception management
✅ **API Integration** - Multiple external service integrations

## 📝 Logging

Application logs are written to `app.log` with DEBUG level detail, capturing:
- API requests and responses
- Agent execution flow
- Error conditions and exceptions
- Tool invocations

## 🔐 Environment Variables

All sensitive configuration (API keys, URLs) is managed through environment variables in a `.env` file, keeping credentials secure and configuration flexible.

## 🎯 Future Enhancements

- Flight booking integration
- Restaurant/activity recommendations
- Weather forecasts for destinations
- Budget estimation and optimization
- Multi-city itinerary planning
- User preferences and travel history
- Mobile app interface
