import json
from files import Files

with open(Files.settings) as f:
    settings = json.load(f)

class Settings:
    developerMode = settings["developerMode"]
    token = settings["token"]
    guildID = settings["guildID"]