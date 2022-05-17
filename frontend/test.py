import os, pathlib

temp = f"{os.path.expanduser('~')}\AppData\Local\Temp\FxWebLauncherPath.wlpy"

if os.path.exists(temp):
    print("ok")
else:
    print("a")
