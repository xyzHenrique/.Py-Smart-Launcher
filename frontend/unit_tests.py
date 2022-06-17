import os, screeninfo

monitors = list()
for monitor in screeninfo.get_monitors():
    monitors.append(monitor)

with open(f"{os.path.expanduser('~')}\AppData\Local\Temp\SmartLauncher.session", "w+") as outfile:
    outfile.write(str(monitors))
