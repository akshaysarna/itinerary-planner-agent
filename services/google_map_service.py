import os
import requests
import logging


#
#  API Calling for the Google Map Service
#
def get_places_details(searchQuery, fieldMask = None):
    url = os.getenv("GOOGLE_MAP_PLACE_API_URL")

    if fieldMask is None:
        fieldMask = ["places.displayName","places.formattedAddress","places.location"]

    #converting list into comma seperated values
    fieldMask = ",".join(fieldMask)
    
    #adding header configurations
    headers = {
        "Content-Type": "application/json", 
        "X-Goog-Api-Key": os.getenv("GOOGLE_API_TOKEN"), 
        "X-Goog-FieldMask": fieldMask
    }

    #payload for api calling...
    payload = {
        "textQuery": searchQuery
    }
    
    response = requests.post(url = url, json = payload, headers = headers, timeout = 5)

    if response.status_code == 200:
        return response.json()
    else:
        logging.exception(f"Google Map API error (HTTP {response.status_code}): {response.text}")
        raise Exception(f"Google Map API error (HTTP {response.status_code}): {response.text}")
