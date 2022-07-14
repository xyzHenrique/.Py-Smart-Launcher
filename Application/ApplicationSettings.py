### NATIVE
import json

### CALL and INITIALIZE LOCAL PACKAGE
structure = json.load(open("Structure"))

def AutomationSettings():
    return json.load(open(structure["Application.Settings"]["dir"]+"/"+"ApplicationAutomationSettings.json"))

def SystemSettings():        
    return json.load(open(structure["Application.Settings"]["dir"]+"/"+"ApplicationSystemSettings.json"))