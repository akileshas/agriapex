from fastapi import APIRouter
from utils.weather import (
    getWeatherDaily,
    getWeatherHourly,
)


routes = APIRouter()


@routes.get("/get_weather_daily")
def get_weather_daily(latitude: float, longitude: float, date: str = None):
    """
    Get daily weather data for a given latitude and longitude.
    """
    res = getWeatherDaily(latitude, longitude, date)
    return res


@routes.get("/get_weather_hourly")
def get_weather_hourly(latitude: float, longitude: float, date: str = None):
    res = getWeatherHourly(latitude, longitude, date)
    return res
