from flask import Flask, request, jsonify
from NearbySearch import searchNearbyPlaces
from ServiceSetup import createService

import os
from os import environ as env

from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv('AUTH0_DOMAIN'),
    os.getenv('AUTH0_API_AUDIENCE')
)
require_auth.register_token_validator(validator)

service = createService()

app = Flask(__name__)

@app.route('/')
def index():
    """No access token required."""
    response = (
        "Hello from a public endpoint! You don't need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)

@app.route('/api', methods=['GET'])
@require_auth(None)
def api():
    #latitude = request.args.get("latitude")
    #longitude = request.args.get("longitude")
    #return searchNearbyPlaces(service, latitude, longitude)

    """A valid access token is required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated to see this."
    )
    return jsonify(message=response)

@app.route("/makeBooking")
@require_auth("read:messages")
def private_scoped():
    """A valid access token and scope are required."""
    response = (
        "Hello from a private endpoint! You need to be"
        " authenticated and have a scope of read:messages to see"
        " this."
    )
    return jsonify(message=response)
