import os, subprocess

from glob import glob

class ApplicationPlugins:
    def __init__(self):
        self.autoexec = True

        self.get_plugins()

    def get_plugins(self):
        folders = glob("./plugins/*", recursive = True)


        for folder in folders:
            
            if os.path.exists(f"{folder}/plugin.exe") or os.path.exists(f"{folder}/plugin.py"):
                path = os.path.abspath(f"{folder}/plugin.exe")
                
                os.system(path)
                

ApplicationPlugins()