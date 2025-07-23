import os

import json

def create_files_from_list(directory_path):
  os.makedirs(directory_path, exist_ok=True)
  for i in range(3, 51):
    file_name = f"level_{i}.json"
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'w') as f:
        data = {}
        json.dump(data, f)
def copy_data(path):
  with open(path + "\level_3.json") as f:
      data = json.load(f)
  for i in range(4, 51):
    with open(f"{path}\level_{i}.json", "w") as f:
        json.dump(data, f)

directory = 'data\Json\Level'


copy_data(directory)