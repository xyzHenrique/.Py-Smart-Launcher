### NATIVE
import json

### CALL and INITIALIZE LOCAL PACKAGE
structure = json.load(open("Structure"))

def ApplicationAutomationSettings():
    return json.load(open(structure["Application.Settings"]["dir"]+"/"+"ApplicationAutomationSettings.json"))

def ApplicationSystemSettings():        
    return json.load(open(structure["Application.Settings"]["dir"]+"/"+"ApplicationSystemSettings.json"))
    