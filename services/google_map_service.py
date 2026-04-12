import os
import requests
import logging

from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

from config import API_CONFIG
from clients.google_maps.request import Payload
from clients.google_maps.place import Place
from clients.google_maps.response import Response


session = requests.Session()

#
#  API Calling for the Google Map Service
#
@retry(
    stop= stop_after_attempt(API_CONFIG.GOOGLE_MAPS_RETRY_ATTEMPTS),
    wait = wait_exponential(multiplier = 1, min =2 , max = 6), 
    before_sleep = before_sleep_log(logging, logging.WARNING),
    reraise = True
)
def get_places_details(searchQuery : str = "", fieldMask : List[str] = None) -> List[Place]:
    

    if not searchQuery or not searchQuery.strip():
        logging.error("Search query cannot be empty")
        raise ValueError("Search query cannot be empty")

    url = os.getenv("GOOGLE_MAP_PLACE_API_URL")
    api_key = os.getenv("GOOGLE_API_TOKEN")

    #validating if the url and api key are present in the environment variables or not
    if not url or not api_key:
        logging.error("Missing required environment variables: GOOGLE_MAP_PLACE_API_URL or GOOGLE_API_TOKEN.")
        raise ValueError("Missing required environment variables: GOOGLE_MAP_PLACE_API_URL or GOOGLE_API_TOKEN.")
   

    #default feild mask if not provided by the user
    if fieldMask is None:
        fieldMask = ["places.displayName","places.formattedAddress","places.location"]

    #converting list into comma seperated values
    fieldMask = ",".join(fieldMask)
    
    
    #adding header configurations
    headers = {
        "Content-Type": "application/json", 
        "X-Goog-Api-Key": api_key, 
        "X-Goog-FieldMask": fieldMask
    }

    #payload for api calling...
    payload = Payload(textQuery = searchQuery)
    
    response = session.post(url = url, json = payload.model_dump(), headers = headers, timeout = API_CONFIG.GOOGLE_MAPS_API_TIMEOUT)

    if response.status_code == 200:
        validated_response = Response.model_validate(response.json())
        if not validated_response.places:
            logging.warning(f"No places found for the search query: {searchQuery}")
            return []
        return validated_response.places
    else:
        logging.error(f"Google Map API error (HTTP {response.status_code}): {response.text}")
        raise Exception(f"Google Map API error (HTTP {response.status_code}): {response.text}")
