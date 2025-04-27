import os
import json


def get_crop_id(crop_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../data/crop_ids.json"
    )
    file_path = os.path.abspath(file_path)

    with open(file_path, "r") as file:
        data: dict = json.load(file)

    crop_id = None
    for key, value in data.items():
        if value == crop_name:
            crop_id = key
            break

    if crop_id is None:
        return {"error": "Crop name not found."}

    return {"crop_id": crop_id}


def get_state_id(state_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../data/state_ids.json"
    )
    file_path = os.path.abspath(file_path)

    with open(file_path, "r") as file:
        data: dict = json.load(file)

    state_id = None
    for key, value in data.items():
        if value == state_name:
            state_id = key
            break

    if state_id is None:
        return {"error": "State name not found."}

    return {"state_id": state_id}
