import pandas as pd

carbonMultiplier = {
    "red meat": 8,
    "grains": 3.7,
    "dairy": 6.3,
    "cellphone": 3.6,
    "TV": 6.8,
    "computer": 4.2,
    "walking": 0,
    "car": 6.5,
    "public transport": 4.3
}

def calculateCO2(columnName, value):
    return carbonMultiplier[columnName.lower()]*value