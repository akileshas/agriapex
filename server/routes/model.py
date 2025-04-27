import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from fastapi import APIRouter
from utils.model import getRecommendations
from utils.splitter import getSplit


routes = APIRouter()


@routes.get("/get_recommendations")
def get_recommendations(stateId: str, cropId: str, N: int , P: int, K: int):
    res = getRecommendations(stateId, cropId, N, P, K)
    return res


@routes.get("/get_split")
def get_split(crop_name: str, total_days: int):
    res = getSplit(crop_name, total_days)
    return res
