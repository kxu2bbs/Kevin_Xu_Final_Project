from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
API_KEY = "ce6735a25bf32755162d705b3e67666b"

@app.route("/")
def hello_world(weather=None):
    return render_template("index.html", weather=weather)

@app.route("/receive_input", methods=["POST"])
def receive_input():
    location = request.form["location"]
    unit = request.form["units"]
    location_data = convert_location_to_coordinates(location)[0]
    weather = get_current_weather_data(location_data["lat"], location_data["lon"], unit)

    ret_unit = unit

    if len(unit) == 0:
        ret_unit = "kelvin"
    elif unit == "metric":
        ret_unit = "celcius"
    else:
        ret_unit = "fahrenheit"

    return render_template("index.html", weather=weather, unit=ret_unit)

def convert_location_to_coordinates(location):
    api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}'
    res = requests.get(api_url)
    return res.json()

def get_current_weather_data(lat, lon, unit):
    api_url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}'
    res = requests.get(api_url)
    return res.json()

@app.errorhandler(404)
def page_not_found(error):
    return "<h1>404, page not found<h1>"
