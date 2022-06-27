"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: Controllers.py
version: 3.0.0
"""
### NATIVE
import os, sys, time, threading, time

### THIRD
import screeninfo

### LOCAL
from ApplicationInformation import Informations
from ApplicationLogger import Logger

class ApplicationController:
    def __init__(self):
        self.command_windows_application_kill = f"takskill /F /IM {Informations['APP_NAME']}* /T >nul 2>&1"
        self.command_windows_engine_kill = "taskkill /F /IM chrome* /T >nul 2>&1"

        

    def application_kill(self):
        

        
        if os.name == "nt":
            os.system(self.command_windows_application_kill)
    
    def application_restart(self):
        if os.name == "nt":
            os.execl(sys.executable, sys.executable, *sys.argv)    
    
    def engine_kill(self):
        if os.name == "nt":
            os.system(self.command_windows_engine_kill)
        
