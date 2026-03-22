import json
import logging

from langchain.tools import tool
from services.search_api import SearchApi
from services.google_map_service import get_places_details

"""
    Tool to Search for airports
"""
@tool
def search_airport_tool(city = ""):
    
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

    if not city or not city.strip():
        raise ValueError("City name cannot be empty")

    logging.debug(f'fetching nearest airports to the {city}')


    places_details = get_places_details(f"Airport near {city}")

    airport_details = SearchApi().get_airport_details(city)
 
    airport_codes = dict()


    for location in airport_details:
        for airport in location.get('airports', []):
            title = str(airport.get("title", "")).lower()
            code = str(airport.get('airport_code',  ""))
            if title:
                airport_codes[title] = code

    airports = []
    
    if places_details:
        for place in places_details.get('places', []):
            name = str(place.get('displayName', {}).get('text', "")).lower()
            location = place.get('location', {})
            address = place.get('formattedAddress', "")
            airportCode = airport_codes.get(name, "")
            name = name.upper()
            
            if len(airports) < 3 and airportCode != "":
                airports.append({
                    'airport_code' : airportCode,
                    'address' : address,
                    'name' : name,
                    'coordinates' : location
                })
            else:
                break
    
    logging.debug(f'fetched airports from google map and search api {len(airports)} for city {city}')

    return json.dumps({
        'airports': airports
    })
