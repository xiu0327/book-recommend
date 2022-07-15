import json

def get_data(path):
    with open(path, 'r', encoding="utf-8") as f:
        jsonData = json.load(f)
    return jsonData