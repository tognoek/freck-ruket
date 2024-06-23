import json

with open("data/map.json", "r") as file:
    data = json.load(file)

print(data)