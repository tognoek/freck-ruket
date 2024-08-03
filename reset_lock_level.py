import json

data = {}
data["01"] = False

for i in range(2, 51):
    name = str(f"{i:02}")
    data[name] = True


with open("data\Json\Level\lock_levels.json", "w") as file:
    json.dump(data, file, indent=4)

with open("data\Json\Level\start.json", "w") as file:
    data = {}
    data["level"] = 1
    data["character"] + "Pink Man"
    json.dump(data, file)