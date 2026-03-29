import os
import requests
import logging
from clients.search_api.response import Response

# Class For Search API...
class SearchApi:

    api_key = ''
    airport_search_url = ''
    flight_search_url = ''

    def __init__(self):
        base_url = os.getenv("SEARCH_API_BASE_URL")
        self.api_key = os.getenv("SEARCH_API_KEY")

        if not base_url or not self.api_key:
            raise ValueError("Missing Properties SEARCH_API_BASE_URL or SEARCH_API_KEY")

        self.airport_search_url = base_url + os.getenv("SEARCH_API_AIRPORT_DETAILS")
        self.flight_search_url = base_url + os.getenv("SEARCH_API_AIRPORT_DETAILS")


    #Get Airport Details by City Name....    
    def get_airport_details(self, city = ""):

        #Service URL
        service_url = self.airport_search_url + "&q={city}&api_key={key}".format(city = city, key = self.api_key)
        
        #Fetching Response From Search API
        response = requests.get(service_url, timeout = 5)
        
        if response.status_code == 200:
            
            
            return Response.model_validate(response.json()).locations

        else:
            logging.error(f"Error While Fetching Airport Response from Search API {city}")
            raise Exception(f"Error While Fetching Airport Response from Search API {city}")

    def get_flight_details(self):
        raise NotImplementedError("Flight details API not yet implemented")
    