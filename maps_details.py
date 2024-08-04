import os
import datetime 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import pandas as pd


# credit to the tutorial followed: https://www.youtube.com/watch?v=lVtu-JWmHOo&t=450s

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

response = service.places().get(
    name="places/ChIJd4V0ClVZwokR5Z_ZiTr_Iso",
    fields="*"
).execute()

response.keys()
df = pd.json_normalize(response)
df.to_csv('place_details.csv', index=False)