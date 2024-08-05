from flask import Flask, jsonify, request
from googleMaps.mapsNearbyPlaces import searchNearbyPlaces

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Peckish home page!"

@app.route('/api', methods=['GET'])
def api():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    return searchNearbyPlaces(latitude, longitude)

if __name__ == '__main__':
    app.run(debug=True)