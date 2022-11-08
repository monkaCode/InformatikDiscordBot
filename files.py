import json

with open(r"data/settings.json") as f:
    settings = json.load(f)

class Files:
    courses = r"data/courses.json"
    subjects = r"data/subjects.json"
    settings = r"data/settings.json"