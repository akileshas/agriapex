import datetime
import json

import requests

url = "https://api.open-meteo.com/v1/forecast"


def interpret_weather_data_hourly(api_data):
    """
    Interprets weather data from an API response and returns a structured dictionary with units.

    Args:
        api_data (dict): The API data in JSON format.

    Returns:
        list[dict]: A list of dictionaries, each containing weather details for a specific time.
    """
    weather_details = []

    # Extract hourly data
    hourly_data = api_data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    humidities = hourly_data.get("relative_humidity_2m", [])
    wind_speeds = hourly_data.get("wind_speed_10m", [])
    precipitations = hourly_data.get("precipitation", [])
    cloud_covers = hourly_data.get("cloud_cover", [])
    precipitation_probs = hourly_data.get("precipitation_probability", [])

    # Map cloud cover and precipitation probability to categorical data
    def get_weather_condition(cloud_cover, precip_prob):
        if precip_prob > 50:
            return "Rainy" if precip_prob < 80 else "Stormy"
        elif cloud_cover > 50:
            return "Cloudy"
        elif precip_prob == 0:
            return "Sunny"
        return "Partially Cloudy"

    # Parse data
    for i in range(len(times)):
        dt = datetime.datetime.fromisoformat(times[i])
        weather_details.append(
            {
                "Date": dt.date().isoformat(),
                "Time": dt.time().isoformat(),
                "Temperature": (
                    [temperatures[i], "°C"] if i < len(temperatures) else [None, "°C"]
                ),
                "Humidity": (
                    [humidities[i], "%"] if i < len(humidities) else [None, "%"]
                ),
                "Wind Speed": (
                    [wind_speeds[i], "m/s"] if i < len(wind_speeds) else [None, "m/s"]
                ),
                "Precipitation": (
                    [precipitations[i], "mm"]
                    if i < len(precipitations)
                    else [None, "mm"]
                ),
                "Condition": get_weather_condition(
                    cloud_covers[i] if i < len(cloud_covers) else 0,
                    precipitation_probs[i] if i < len(precipitation_probs) else 0,
                ),
            }
        )

    return weather_details


def getWeatherHourly(latitude, longitude, date=None):
    if date == None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    # print(date)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,cloud_cover,wind_speed_10m,wind_direction_10m",
        "forecast_days": 16,
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    # return data
    return interpret_weather_data_hourly(data)


def interpret_daily_weather_data(api_data):
    """
    Interprets daily aggregated weather data from an API response and returns structured data with units.

    Args:
        api_data (dict): The API data in JSON format.

    Returns:
        list[dict]: A list of dictionaries, each containing daily aggregated weather details with units.
    """
    weather_details = []

    # Extract hourly data
    hourly_data = api_data.get("hourly", {})
    times = hourly_data.get("time", [])
    temperatures = hourly_data.get("temperature_2m", [])
    humidities = hourly_data.get("relative_humidity_2m", [])
    wind_speeds = hourly_data.get("wind_speed_10m", [])
    precipitations = hourly_data.get("precipitation", [])
    cloud_covers = hourly_data.get("cloud_cover", [])
    precipitation_probs = hourly_data.get("precipitation_probability", [])

    # Dictionary to group data by date
    daily_data = {}

    # Map cloud cover and precipitation probability to categorical data
    def get_weather_condition(cloud_cover, precip_prob):
        if precip_prob > 50:
            return "Rainy" if precip_prob < 80 else "Stormy"
        elif cloud_cover > 50:
            return "Cloudy"
        elif precip_prob == 0:
            return "Sunny"
        return "Partially Cloudy"

    # Group data by date and calculate daily maximums
    for i, time_str in enumerate(times):
        dt = datetime.datetime.fromisoformat(time_str)
        date = dt.date().isoformat()

        if date not in daily_data:
            daily_data[date] = {
                "Temperature": float("-inf"),
                "Humidity": float("-inf"),
                "Wind Speed": float("-inf"),
                "Precipitation": float("-inf"),
                "Conditions": [],
            }

        # Update daily maximum values
        daily_data[date]["Temperature"] = max(
            daily_data[date]["Temperature"], temperatures[i]
        )
        daily_data[date]["Humidity"] = max(daily_data[date]["Humidity"], humidities[i])
        daily_data[date]["Wind Speed"] = max(
            daily_data[date]["Wind Speed"], wind_speeds[i]
        )
        daily_data[date]["Precipitation"] = max(
            daily_data[date]["Precipitation"], precipitations[i]
        )

        # Add condition for the current hour
        condition = get_weather_condition(
            cloud_covers[i] if i < len(cloud_covers) else 0,
            precipitation_probs[i] if i < len(precipitation_probs) else 0,
        )
        daily_data[date]["Conditions"].append(condition)

    # Prepare the final list of daily weather details
    for date, values in daily_data.items():
        weather_details.append(
            {
                "Date": date,
                "Max Temperature": [values["Temperature"], "°C"],
                "Max Humidity": [values["Humidity"], "%"],
                "Max Wind Speed": [values["Wind Speed"], "m/s"],
                "Max Precipitation": [values["Precipitation"], "mm"],
                "Overall Condition": max(
                    set(values["Conditions"]), key=values["Conditions"].count
                ),  # Most common condition
            }
        )

    return weather_details


def getWeatherDaily(latitude, longitude, date=None):
    if date == None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    # print(date)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,cloud_cover,wind_speed_10m,wind_direction_10m",
        "forecast_days": 16,
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(url, params=params)
    data = response.json()
    # print(data)
    # return data
    return interpret_daily_weather_data(data)


if __name__ == "__main__":
    pass
    # print(getWeatherHourly(12.9716, 77.5946))
    # print(getWeatherDaily(12.9716, 77.5946))
