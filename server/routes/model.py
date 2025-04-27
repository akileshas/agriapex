from fastapi import APIRouter
from utils.model import getRecommendations


routes = APIRouter()


@routes.get("/get_recommendations")
def get_recommendations(stateId: str, cropId: str, N: int , P: int, K: int):
    res = getRecommendations(stateId, cropId, N, P, K)
    return res
