import os
import sys
import torch

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from models.minn import MINN


input_dim = 512
output_dim = 10
model = MINN(input_dim=input_dim, output_dim=output_dim)

model_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "../models/weights/minn.pth"
))
model.load_weights(model_path)


def generateInputTensor(state_id: str, crop_id: str, rows: int = 32, cols: int = 512):
    state_num = int(state_id, 16)
    crop_num = int(crop_id, 16)

    tensor = torch.rand(rows, cols)

    state_tensor = torch.tensor([state_num], dtype=torch.float32)
    crop_tensor = torch.tensor([crop_num], dtype=torch.float32)

    tensor[:, 0] = state_tensor
    tensor[:, 1] = crop_tensor

    return tensor


def calculateValue(minThreshold, maxThreshold, minValue, maxValue, currentIndex):
    minThreshold = float(minThreshold)
    maxThreshold = float(maxThreshold)
    minValue = float(minValue)
    maxValue = float(maxValue)
    currentIndex = float(currentIndex)
    if currentIndex < minThreshold:
        return minValue
    if currentIndex > maxThreshold:
        return maxValue
    # return (maxValue - minValue) / (maxThreshold - minThreshold) * (currentIndex - minThreshold) + minValue
    return round((maxValue - minValue) / (maxThreshold - minThreshold) * (currentIndex - minThreshold) + minValue, 2)



def getRecommendations(stateId: str, cropId: str, N: int , P: int, K: int):
    global model
    input_tensor = generateInputTensor(stateId, cropId)
    output = model(input_tensor)
    if stateId not in output:
        return "State not found"
    if cropId not in output[stateId]:
        return "Crop not found"
    if "N" not in output[stateId][cropId]:
        return "N not found"
    else:
        minThreshold_N = min(output[stateId][cropId]["N"].keys())
        maxThreshold_N = max(output[stateId][cropId]["N"].keys())
        minValue_N = output[stateId][cropId]["N"][minThreshold_N][0]
        maxValue_N = output[stateId][cropId]["N"][maxThreshold_N][0]
        unit_N = output[stateId][cropId]["N"][minThreshold_N][1]
    if "P" not in output[stateId][cropId]:
        return "P not found"
    else:
        minThreshold_P = min(output[stateId][cropId]["P"].keys())
        maxThreshold_P = max(output[stateId][cropId]["P"].keys())
        minValue_P = output[stateId][cropId]["P"][minThreshold_P][0]
        maxValue_P = output[stateId][cropId]["P"][maxThreshold_P][0]
        unit_P = output[stateId][cropId]["P"][minThreshold_P][1]
    if "K" not in output[stateId][cropId]:
        return "K not found"
    else:
        minThreshold_K = min(output[stateId][cropId]["K"].keys())
        maxThreshold_K = max(output[stateId][cropId]["K"].keys())
        minValue_K = output[stateId][cropId]["K"][minThreshold_K][0]
        maxValue_K = output[stateId][cropId]["K"][maxThreshold_K][0]
        unit_K = output[stateId][cropId]["K"][minThreshold_K][1]
    Urea = [calculateValue(minThreshold_N, maxThreshold_N, minValue_N, maxValue_N, N), unit_N]
    DAP = [calculateValue(minThreshold_P, maxThreshold_P, minValue_P, maxValue_P, P), unit_P]
    MOP = [calculateValue(minThreshold_K, maxThreshold_K, minValue_K, maxValue_K, K), unit_K]
    # return recN, recP, recK
    return {
        "Urea": Urea,
        "DAP": DAP,
        "MOP": MOP
    }

if __name__ == "__main__":
    stateId = "63f9ce47519359b7438e76fa"
    cropId = "654494c2d481b13d70e3a36e"
    print(getRecommendations(stateId, cropId, 0, 0, 0))
    print(getRecommendations(stateId, cropId, 100, 100, 100))
    print(getRecommendations(stateId, cropId, 701, 41, 561))
