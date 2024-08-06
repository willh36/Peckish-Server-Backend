from flask import Flask, jsonify, request
from NearbySearch import searchNearbyPlaces
from ServiceSetup import createService

service = createService()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Peckish home page!"

@app.route('/api', methods=['GET'])
def api():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    return searchNearbyPlaces(service, latitude, longitude)