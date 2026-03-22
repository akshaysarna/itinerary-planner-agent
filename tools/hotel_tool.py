import json
import logging

from langchain.tools import tool
from services.google_map_service import get_places_details

"""
    Tool for Searching hotels
"""
@tool
def search_hotel_tool(city = ""):

    """
        Searches hotels in a given city or location using Google Maps data.
        Use this tool when:
        - You need to find hotels options for a destination/location
        - You want hotels Details such as Address, Ratings and Operational Details
        - You are Selecting hotels for Itinerary

        Input:
        - location(string): Name of City, Area (e.g. "Goa", "South Goa")

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

    if not city or not city.strip():
        raise ValueError("City name cannot be empty")

    logging.debug(f'fetching hotels to the {city}')

    places = get_places_details(f"Hotels in {city}", ["places.displayName"
    ,"places.formattedAddress","places.types","places.rating","places.regularOpeningHours.weekdayDescriptions", "places.location"])

    hotels = []

    #Sorting Hotels By Ratings
    hotels_details = sorted(places.get('places', []), key = lambda hotel: hotel.get('rating', 0), reverse = True)


    for hotel in hotels_details:

        name = str(hotel.get('displayName', {}).get('text', "")).lower()
        location = hotel.get('location', {})
        address = hotel.get('formattedAddress', "")
        rating = hotel.get('rating', 0.0)

        if len(hotels) < 6:
            hotels.append({
                'name': name,
                'coordinates': location,
                'address' : address,
                'rating': rating
            })
        else:
            break
        
    logging.debug(f'fetched hotels to the {hotels}')

    return json.dumps({
        'hotels': hotels
    })
    
