import requests


base_url = "http://127.0.0.1:8000"


def get_states():
    res = requests.get(f"{base_url}/data/get_states")
    if res.ok:
        states = res.json()["states"]
        return states
    return []


def get_crops(state_name, state=False):
    res = requests.get(
        (
            f"{base_url}/data/get_crops_for_state"
            if state else f"{base_url}/data/get_crops"
        ),
        params={
            "state_name": state_name,
        }
    )
    if res.ok:
        crops = res.json()["crops"]
        return crops
    return []


def get_state_id(state_name):
    res = requests.get(
        f"{base_url}/data/get_state_id",
        params={"state_name": state_name}
    )
    if res.ok:
        state_id = res.json()["state_id"]
        return state_id
    return ""


def get_crop_id(crop_name):
    res = requests.get(
        f"{base_url}/data/get_crop_id",
        params={"crop_name": crop_name}
    )
    if res.ok:
        crop_id = res.json()["crop_id"]
        return crop_id
    return ""


def get_soil_types():
    soil_types = [
        "Clay",
        "Sandy",
        "Loamy",
        "Silty",
        "Peaty",
        "Chalky"
    ]
    return soil_types


def get_recommendations(state_id, crop_id, N, P, K):
    res = requests.get(
        f"{base_url}/model/get_recommendations",
        params={
            "stateId": state_id,
            "cropId": crop_id,
            "N": N,
            "P": P,
            "K": K,
        }
    )
    return res.json()


def get_schedule(recommendation, crop_name, total_days, sowing_date):
    res = requests.get(
        f"{base_url}/model/get_schedule",
        params={
            "Urea": int(recommendation["Urea"][0]),
            "DAP": int(recommendation["DAP"][0]),
            "MOP": int(recommendation["MOP"][0]),
            "unit": "Kg per Hectare",
            "crop_name": crop_name,
            "total_days": total_days,
            "sowing_date": sowing_date,
        }
    )
    return res.json()
