import json

with open("data/Json/data_characters.json", "r") as file:
    data = json.load(file)

print(len(data["Points Collision"]["Main Characters"]["Mask Dude"]["Run"]))