import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

def searchNearbyPlaces(latitude, longitude):      
    ###### ---------------- CREATE SERVICE ---------------- ######
    CLIENT_SECRET_FILE = 'client-secret.json'
    API_SERVICE_NAME = 'places'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    prefix = ''

    creds = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
    except Exception as e:
        print(e)
        print(f'Failed to create service for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, token_file))

    ###### ---------------- END OF SERVICE CREATION ---------------- ######


    request_body = { # make request body (what you want to search for)
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

    response = service.places().searchNearby( # make the request and specify what fields you want returned
        body=request_body,
        fields="places.id,places.displayName,places.businessStatus,places.websiteUri,places.location,places.accessibilityOptions"
    ).execute()

    return response

#print(response) # output the response
