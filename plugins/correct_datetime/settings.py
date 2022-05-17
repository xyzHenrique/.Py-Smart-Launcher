import json

def PluginSettings():
    data = json.load(open("./settings.json"))

    return data