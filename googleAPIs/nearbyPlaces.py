import os
from dotenv import load_dotenv
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.auth import identity_pool, impersonated_credentials
from google.auth.transport.requests import Request
from google.auth import exceptions
from googleapiclient.discovery import build

load_dotenv()

def searchNearbyPlaces(latitude, longitude):
    ###### ---------------- CREATE SERVICE ---------------- ######
    API_SERVICE_NAME = 'places'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    # Load environment variables
    project_id = os.getenv("GCP_PROJECT_ID")
    project_number = os.getenv("GCP_PROJECT_NUMBER")
    service_account_email = os.getenv("GCP_SERVICE_ACCOUNT_EMAIL")
    workload_identity_pool_id = os.getenv("GCP_WORKLOAD_IDENTITY_POOL_ID")
    workload_identity_pool_provider_id = os.getenv("GCP_WORKLOAD_IDENTITY_POOL_PROVIDER_ID")

    # Authenticate using Workload Identity Federation
    try:
        # Build the audience
        audience = f"//iam.googleapis.com/projects/{project_number}/locations/global/workloadIdentityPools/{workload_identity_pool_id}/providers/{workload_identity_pool_provider_id}"

        # Generate the credentials for the service account
        credentials = identity_pool.Credentials.from_info(
            audience=audience,
            target_principal=service_account_email,
            target_scopes=SCOPES
        )

        # Use impersonated credentials if necessary
        target_credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=service_account_email,
            target_scopes=SCOPES
        )

        # Create the service
        service = build(API_SERVICE_NAME, API_VERSION, credentials=target_credentials, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')

    except exceptions.GoogleAuthError as e:
        print(f'Failed to create service for {API_SERVICE_NAME}: {str(e)}')
        return None

    ###### ---------------- END OF SERVICE CREATION ---------------- ######

    request_body = {  # make request body (what you want to search for)
        "includedTypes": ["american_restaurant", "bakery", "bar", "barbecue_restaurant", "brazilian_restaurant", 
                          "breakfast_restaurant", "brunch_restaurant", "cafe", "chinese_restaurant", "coffee_shop", 
                          "fast_food_restaurant", "french_restaurant", "greek_restaurant", "hamburger_restaurant", 
                          "ice_cream_shop", "indian_restaurant", "indonesian_restaurant", "italian_restaurant", 
                          "japanese_restaurant", "korean_restaurant", "lebanese_restaurant", "meal_delivery", 
                          "meal_takeaway", "mediterranean_restaurant", "mexican_restaurant", "middle_eastern_restaurant", 
                          "pizza_restaurant", "ramen_restaurant", "restaurant", "sandwich_shop", "seafood_restaurant", 
                          "spanish_restaurant", "steak_house", "sushi_restaurant", "thai_restaurant", 
                          "turkish_restaurant", "vegan_restaurant", "vegetarian_restaurant", "vietnamese_restaurant"],
        "excludedTypes": ["preschool", "primary_school", "secondary_school", "church", "hindu_temple", "mosque", 
                          "synagogue"],
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

    try:
        response = service.places().searchNearby(
            body=request_body,
            fields="places.id,places.displayName,places.businessStatus,places.websiteUri,places.location,places.accessibilityOptions"
        ).execute()

        return response

    except Exception as e:
        print(f"Failed to execute searchNearbyPlaces: {str(e)}")
        return None
    
print(searchNearbyPlaces(40.477398, -74.259087))