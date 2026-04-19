import os
import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from config import API_CONFIG
from clients.search_api.response import Response

session = requests.Session()

# Class For Search API...
class SearchApi:

    search_api_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.search_api_instance is None:
            cls.search_api_instance = super().__new__(cls)
        return cls.search_api_instance

    def __init__(self):
        if not getattr(self, '_initialized', False):
            base_url = os.getenv("SEARCH_API_BASE_URL")
            self.api_key = os.getenv("SEARCH_API_KEY")

            if not base_url or not self.api_key:
                raise ValueError("Missing Properties SEARCH_API_BASE_URL or SEARCH_API_KEY")

            self.airport_search_url = base_url + os.getenv("SEARCH_API_AIRPORT_DETAILS")
            self._initialized = True
            

    #Get Airport Details by City Name....    
    @retry(
        stop= stop_after_attempt(API_CONFIG.SEARCH_API_RETRY_ATTEMPTS), 
        wait = wait_exponential(multiplier = 1, min =2 , max = 6), 
        before_sleep = before_sleep_log(logging, logging.WARNING),
        reraise = True
    )
    def get_airport_details(self, city = ""):

        #Service URL
        service_url = self.airport_search_url + "&q={city}&api_key={key}".format(city = city, key = self.api_key)
        
        #Fetching Response From Search API
        response = session.get(service_url, timeout = API_CONFIG.SEARCH_API_TIMEOUT)
        
        if response.status_code == 200:
            
            
            return Response.model_validate(response.json()).locations

        else:
            logging.error(f"Error While Fetching Airport Response from Search API {city}")
            raise Exception(f"Error While Fetching Airport Response from Search API {city}")

    def get_flight_details(self):
        raise NotImplementedError("Flight details API not yet implemented")
    