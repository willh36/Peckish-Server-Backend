import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

googleApplicationCredentialsDictionary = {
    "type": "service_account",
    "project_id": os.getenv('GCP_PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY').replace('|', '\n'),
    "client_email": os.getenv('GCP_SERVICE_ACCOUNT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
    "universe_domain": "googleapis.com"
}

# Define the writable directory
writable_directory = '/app/writable'
file_name = os.path.join(writable_directory, 'googleCredentials.json')

with open(file_name, 'w') as file:
    json.dump(googleApplicationCredentialsDictionary, file, indent=4)

def createService():
    # Load credentials from the service account key JSON file
    credentials = service_account.Credentials.from_service_account_file(
        file_name, 
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    # Build the API client
    service = build('places', 'v1', credentials=credentials, static_discovery=False)
    return service
