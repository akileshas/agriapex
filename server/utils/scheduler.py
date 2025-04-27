import os
import sys
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from utils.splitter import getSplit


"""
NPK Ratios
DAP - 18:46:0
MOP - 0:0:60
Urea - 46:0:0
"""


def getGroundTruth(Urea, DAP, MOP):
    N, P, K = 0,0,0
    N = (Urea*46)/100
    N += (DAP*18)/100
    P = (DAP*46)/100
    K = (MOP*60)/100
    return N,P,K


def getRecommendation(N,P,K, unit):
    DAP, MOP, Urea = 0,0,0
    DAP = (P*100)/46
    N -= (DAP*18)/100
    MOP = (K*100)/60
    Urea = (N*100)/46
    return [round(Urea, 2), unit], [round(DAP, 2), unit], [round(MOP, 2), unit]


def getSchedule(Urea, DAP, MOP, unit, crop_name, total_days, sowing_date):
    stages = getSplit(crop_name, total_days)
    # print(stages)
    N, P, K = getGroundTruth(Urea, DAP, MOP)
    stage_wise_requirements = {}
    for stage in stages['stages']:
        list = []
        list.append(stages['stages'][stage][0])
        getList = getRecommendation(N*(stages['stages'][stage][2]/100), P*(stages['stages'][stage][3]/100), K*(stages['stages'][stage][4]/100), unit)
        list.append(getList[0])
        list.append(getList[1])
        list.append(getList[2])
        stage_wise_requirements[stage] = list

    start_date = sowing_date
    for stage in stage_wise_requirements:
        days = stages['stages'][stage][1]
        stage_wise_requirements[stage].append(days)
        stage_wise_requirements[stage].append(start_date)
        start_date = time.strftime("%Y-%m-%d", time.gmtime(time.mktime(time.strptime(start_date, "%Y-%m-%d")) + days*24*60*60))
        stage_wise_requirements[stage].append(start_date)
    return stage_wise_requirements


if __name__ == "__main__":
    ferti_total_requirements = {
        "Urea": [
            677.9,
            "Kg per Hectare"
        ],
        "DAP": [
            101.14,
            "Kg per Hectare"
        ],
        "MOP": [
            331.12,
            "Kg per Hectare"
        ]
    }

    Urea = ferti_total_requirements['Urea'][0]
    DAP = ferti_total_requirements['DAP'][0]
    MOP = ferti_total_requirements['MOP'][0]
    unit = ferti_total_requirements['Urea'][1]
    current_date = time.strftime("%Y-%m-%d")
    sowing_date = "2024-12-07"
    print(getSchedule(Urea, DAP, MOP, unit, "paddy", 140, sowing_date))
