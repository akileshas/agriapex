import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from fastapi import APIRouter
from utils.data import (
    get_state_id,
    get_crop_id,
)


routes = APIRouter()


@routes.get("/get_crops")
def get_crops():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../data/crop_ids.json"
    )
    file_path = os.path.abspath(file_path)

    with open(file_path, "r") as file:
        data: dict = json.load(file)

    res = {
        "crops": list(data.values())
    }
    return res


@routes.get("/get_states")
def get_states():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../data/state_ids.json"
    )
    file_path = os.path.abspath(file_path)

    with open(file_path, "r") as file:
        data: dict = json.load(file)

    res = {
        "states": list(data.values())
    }
    return res


@routes.get("/get_crops_for_state")
def get_crops_for_state(state_name: str):
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../data/state_crop_ids.json"
    )
    file_path = os.path.abspath(file_path)

    with open(file_path, "r") as file:
        data: dict = json.load(file)

    state_id = get_state_id(state_name)["state_id"]
    state_crops = data.get(state_id, [])

    res = {
        "crops": list(state_crops.values())
    }
    return res


@routes.get("/get_state_id")
def get_state_id_route(state_name: str):
    res = get_state_id(state_name)
    return res


@routes.get("/get_crop_id")
def get_crop_id_route(crop_name: str):
    res = get_crop_id(crop_name)
    return res
