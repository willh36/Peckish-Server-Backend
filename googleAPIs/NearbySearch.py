import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from GoogleAPIs.ServiceSetup import createService


def searchNearbyPlaces(service, latitude, longitude):
    request_body = {  # make request body (what you want to search for)
        "includedTypes": ["american_restaurant", "bakery", "bar", "barbecue_restaurant", "brazilian_restaurant", "breakfast_restaurant", "brunch_restaurant", "cafe", "chinese_restaurant", "coffee_shop", "fast_food_restaurant", "french_restaurant", "greek_restaurant", "hamburger_restaurant", "ice_cream_shop", "indian_restaurant", "indonesian_restaurant", "italian_restaurant", "japanese_restaurant", "korean_restaurant", "lebanese_restaurant", "meal_delivery", "meal_takeaway", "mediterranean_restaurant", "mexican_restaurant", "middle_eastern_restaurant", "pizza_restaurant", "ramen_restaurant", "restaurant", "sandwich_shop", "seafood_restaurant", "spanish_restaurant", "steak_house", "sushi_restaurant", "thai_restaurant", "turkish_restaurant", "vegan_restaurant", "vegetarian_restaurant", "vietnamese_restaurant"],
        "excludedTypes": ["preschool", "primary_school", "secondary_school", "church", "hindu_temple", "mosque", "synagogue"],
        "maxResultCount": 10,
        "rankPreference": "DISTANCE",
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude},
                "radius": 5000.0
            }
        }
    }

    response = service.places().searchNearby(  # make the request and specify what fields you want returned
        body=request_body,
        fields="places.id,places.displayName,places.businessStatus,places.websiteUri,places.location,places.accessibilityOptions"
    ).execute()

    return response


#service = create_service()
#print(searchNearbyPlaces(service, 40.477398, -74.259087))