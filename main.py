from dotenv import load_dotenv
import asyncio
import logging
from agents.itinerary_agent import itinerary_agent

#Loading Dot Env File
load_dotenv()

#Adding Logging Framework....
logging.basicConfig(filename = "app.log", level = logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

#Run Itinerary Agent in Async Mode
asyncio.run(itinerary_agent())