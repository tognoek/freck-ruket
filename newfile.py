import os

import json

def create_files_from_list(directory_path):
  """Tạo các file mới dựa trên danh sách tên file và đường dẫn thư mục

  Args:
    file_names: Danh sách các tên file cần tạo.
    directory_path: Đường dẫn đến thư mục đích.
  """

  # Tạo thư mục nếu chưa tồn tại
  os.makedirs(directory_path, exist_ok=True)

  # Tạo từng file
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