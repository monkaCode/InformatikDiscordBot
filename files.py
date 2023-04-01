import json

with open(r"data/settings.json") as f:
    settings = json.load(f)

class Files:
    settings = r"data/settings.json"