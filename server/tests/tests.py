import json
import requests

# user inputs
layout = {
    "state": "TAMIL NADU",                  # cat       (req)
    "crop": "blackgramrainfed",             # cat       (req)
    "area": 150,                            # sq mtr    (opt)
    "total_days": 100,                      # int       (opt)
    "sowing_date": "2024-12-07",            # date      (opt)
    "soil": "Clay",                         # cat       (opt)
}
soil_content = {
    "n": 150.0,                             # kg/ha     (req)
    "p": 100.0,                             # kg/ha     (req)
    "k": 100.0,                             # kg/ha     (req)
    "moisture": 50,                         # %         (opt)
    "ph": 7,                                # ratio     (opt)
}
loc = {
    "lat": 13.0843,                         # deg       (req)
    "lon": 80.2705,                         # deg       (req)
}

base_url = "http://127.0.0.1:8000"

# workflow
# step 1
state_id = requests.get(
    f"{base_url}/data/get_state_id",
    params={
        "state_name": layout["state"],
    }
)
crop_id = requests.get(
    f"{base_url}/data/get_crop_id",
    params={
        "crop_name": layout["crop"],
    }
)
# print(state_id.json())
# print(crop_id.json())

# step 2
reccommendation = requests.get(
    f"{base_url}/model/get_recommendations",
    params={
        "stateId": state_id.json()["state_id"],
        "cropId": crop_id.json()["crop_id"],
        "N": soil_content["n"],
        "P": soil_content["p"],
        "K": soil_content["k"],
    },
)
# print(reccommendation.json())

# step 3
schedule = requests.get(
    f"{base_url}/model/get_schedule",
    params={
        "Urea": int(reccommendation.json()["Urea"][0]),
        "DAP": int(reccommendation.json()["DAP"][0]),
        "MOP": int(reccommendation.json()["MOP"][0]),
        "unit": "Kg per Hectare",
        "crop_name": layout["crop"],
        "total_days": layout["total_days"],
        "sowing_date": layout["sowing_date"],
    }
)
print(json.dumps(schedule.json(), indent=2))
