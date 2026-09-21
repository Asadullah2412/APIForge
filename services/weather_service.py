# generates fake data 
from fastapi import status
city_detailed_weather = {
    "Doha": {
        "temp": 35,
        "condition": "Clear",
        "humidity": 63
    },
    "London": {
        "temp": 19,
        "condition": "Rainy",
        "humidity": 82
    },
    "Tokyo": {
        "temp": 23,
        "condition": "Cloudy",
        "humidity": 55
    },
    "New York": {
        "temp": 22,
        "condition": "Windy",
        "humidity": 48
    },
    "Sydney": {
        "temp": 16,
        "condition": "Sunny",
        "humidity": 60
    },
    "Paris": {
        "temp": 18,
        "condition": "Misty",
        "humidity": 75
    },
    "Cairo": {
        "temp": 31,
        "condition": "Sunny",
        "humidity": 40
    },
    "Reykjavik": {
        "temp": 6,
        "condition": "Snowy",
        "humidity": 88
    },
    "Mumbai": {
        "temp": 29,
        "condition": "Thundery",
        "humidity": 85
    },
    "Singapore": {
        "temp": 30,
        "condition": "Humid",
        "humidity": 90
    }
}

def get_weather(city:str):
    if city.title() in city_detailed_weather:
        return {"weather": city_detailed_weather[city.title()]}
    else:
        raise ValueError("City not found")



# temp = get_weather(city="new york")
# print(temp)

    
