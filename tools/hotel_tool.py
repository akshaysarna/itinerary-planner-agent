import json
import logging

from typing import List
from pydantic import TypeAdapter

from langchain.tools import tool

from config import API_CONFIG
from validation import valid_city
from services.google_map_service import get_places_details
from models.internal.hotel import Hotel
from models.internal.location import Location

"""
    Tool for Searching hotels
"""
@tool
def search_hotel_tool(city: str = "") -> str:

    """
        Searches hotels in a given city or location using Google Maps data.
        Use this tool when:
        - You need to find hotels options for a destination/location
        - You want hotels Details such as Address, Ratings and Operational Details
        - You are Selecting hotels for Itinerary

        Input:
        - city(string): Name of City, Area (e.g. "Goa", "South Goa")

        Returns:
        List of hotels with Following Details:
        - name
        - address
        - coordinates (latitude, longitude)
        - rating
        
        Constraints:
        - Prefer hotels with Ratings >= 3.5
        - Limit Results to 5-10 relevant hotels
        
        Important:
        - Avoid Calling Tools Multiple Times for the Same ResultSet
        - Use results from this tool to make informed decision about accomodations selection
    """

    if not valid_city(city):
        raise ValueError("City name cannot be empty")

    logging.debug(f'fetching hotels to the {city}')

    places = get_places_details(f"Hotels in {city}", ["places.displayName"
    ,"places.formattedAddress","places.types","places.rating","places.regularOpeningHours.weekdayDescriptions", "places.location"])

    #Sorting Hotels By Ratings
    hotels_details = sorted(places, key = lambda hotel: hotel.rating, reverse = True)

    hotels: List[Hotel] = []
    
    for hotel in hotels_details:

        name = hotel.displayNameText
        location = hotel.location
        address = hotel.formattedAddress
        rating = hotel.rating

        if API_CONFIG.HOTEL_MAX_RESULTS > len(hotels):
            coordinates = Location(latitude = location.latitude, longitude = location.longitude) if location else None
            hotels.append(Hotel(name = name, address = address, rating = rating, coordinates = coordinates))
        else:
            break
        
    logging.debug(f'fetched hotels to the {hotels}')

    adapter = TypeAdapter(List[Hotel])

    return json.dumps({
        'hotels': adapter.dump_python(hotels)
    })
    
