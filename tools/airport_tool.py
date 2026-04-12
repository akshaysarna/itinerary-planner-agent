import json
import logging
from typing import List
from pydantic import TypeAdapter
from langchain.tools import tool


from config import API_CONFIG
from validation import valid_city
from services.search_api import SearchApi
from services.google_map_service import get_places_details

from models.internal.airport import Airport
from models.internal.location import Location

"""
    Tool to Search for airports
"""
@tool
def search_airport_tool(city: str = "") -> str:
    
    """
        Search for airports near a given city or location using Google Maps data
        Use this tool when:
        - You need to find airports serving the city or nearby regions
        - You are selecting arrival or departure points for travel planning
        
        Input:
        city(string): Name of City, Area (e.g. "Delhi", "Noida")

        Returns:
        A list of the airports
        - name
        - address
        - coordinates (longitude/latitude)
        - airport_code

        Constraints:
        - Prefer airports closest to the itinerary location
        - Limit results to 1-3 relevant airports 

        Important:
        - Avoid Calling tools several times for the same city unless necessary
        - Use results of the tool to select the most appropriate airport for the itinerary
    """

    if not valid_city(city):
        raise ValueError("City name cannot be empty")

    logging.debug(f'fetching nearest airports to the {city}')


    places = get_places_details(f"Airport near {city}")

    airport_details = SearchApi().get_airport_details(city)
 
    airport_codes = dict()


    for location in airport_details:
        for airport in location.airports:
            title = str(airport.title).lower()
            code = str(airport.airport_code)
            if title:
                airport_codes[title] = code

    airports : List[Airport] = []
    
    if places:
        for place in places:
            
            #Using Display Name as key to match the airport code from search api response as google map api does not provide airport code in response
            key = str(place.displayNameText).lower()
            location = place.location
            address = place.formattedAddress
            airportCode = airport_codes.get(key, "")
            name = place.displayNameText

            if API_CONFIG.AIRPORT_MAX_RESULTS >= len(airports) and airportCode != "":
                coordinates = Location(latitude = location.latitude, 
                    longitude = location.longitude) if location else None
                        
                airports.append(
                    Airport(
                        airport_code = airportCode,    
                        address = address,     
                        name = name,    
                        coordinates = coordinates
                    )
                )
            
            if API_CONFIG.AIRPORT_MAX_RESULTS == len(airports):
                break


    logging.debug(f'fetched airports from google map and search api {len(airports)} for city {city}')

    adapter = TypeAdapter(List[Airport])

    return json.dumps({
        'airports': adapter.dump_python(airports)
    })
