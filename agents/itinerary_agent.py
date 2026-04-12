import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from llm.claude import get_claude_llm

from tools.airport_tool import search_airport_tool
from tools.hotel_tool import search_hotel_tool

async def itinerary_agent():
    llm = get_claude_llm()

    tools = [search_airport_tool, search_hotel_tool]

    #Chat Prompt Template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
            You are a professional Travel Planning Assistant
            Your goal is to assist user plans trip using the available tool and provide structured,
            Think step-by-step and use tools before answering.
            When a user ask about planning a trip, you Must follow these steps:
            1 Identify the destination from the user query.
            2 Call 'search_airport_tool' to look for the nearest airport to the destination.
            3 Call 'search_hotel_tool' to find the suitable hotels in the destination.
            4 Combine the result from the tools and generate a clear itinerary.

            Tool Usage Rules:
            - Use tools only when required to fetch missing information.
            - Call each tool at most once per request.
            - Do NOT call the same tool again with the same input.

            Completion Rule:
            - After all required tool data is obtained, STOP calling tools.
            - Use the collected data to generate the final response.
            - Do NOT call any tool after starting the final answer.

            Output Format (strict):
            - Destination: <city>
            - Nearest Airport: <name + code or "Not Found">
            - Recommended Hotels (prefer rating):
                1. <Hotel Name>  (Rating: <rating>)
                2. <Hotel Name>  (Rating: <rating>)
            - suggest itinerary (day-wise or summary)
                1. Day 1: ...
                2. Day 2: ...
        """),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    #create agent with tools
    agent = create_tool_calling_agent(llm, tools, prompt_template)
    
    #adding memory
    memory = ConversationBufferWindowMemory(k = 5, memory_key = "chat_history", return_messages = True, output_key = "output") 

    #creating agent_executor
    agent_executor = AgentExecutor(agent = agent, tools = tools,  memory = memory, verbose = False)

    prompt = input("Welcome to Itinerary Portal \n").strip()
    
    while prompt != '0':
        try:
            #Streaming Response from Agent in Console
            async for event in agent_executor.astream_events({'input': prompt}, version= "v1"):
                event_type = event.get('event', "")
                if event_type == "on_chat_model_stream":
                    try:
                        chunk = event.get('data', {})['chunk']
                        if chunk and hasattr(chunk, 'content') and chunk.content:
                            for block in chunk.content:
                                if isinstance(block, dict) and block.get('type')== 'text': 
                                    print(block.get('text'), end="", flush=True)
                    except Exception as e:
                        logging.exception(f"Error processing stream chunk: {str(e)}")
        except Exception as e:
            logging.exception(f"Agent Execution Error : {str(e)}")
        
        prompt = input("\n Provide Query or Enter 0 for Exit \n").strip()