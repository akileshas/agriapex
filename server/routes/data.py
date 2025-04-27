import os
import json
import utils
import pandas as pd
from fastapi import APIRouter


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

    res = list(data.values())
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

    res = list(data.values())
    return res
