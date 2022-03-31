import requests, urllib3, time, ctypes, sys

from win32 import win32api
from pandas import Timestamp
from datetime import datetime, timezone

from settings import PluginSettings

class correct_datetime:
    def __init__(self):
        self.plugin_settings = PluginSettings()

        self.URL = self.plugin_settings["DATETIME"][".URL"]
        self.SSL = self.plugin_settings["DATETIME"][".SSL"]

        self.date = {"day": None, "month": None, "year": None} 
        self.time = {"hour": None, "minute": None, "second": None, "millseconds": 0}

        if self.plugin_settings["DATETIME"][".ENABLED"]:
            print("'plugin - correct date/time' - criado por: Henrique Rodrigues Pereira\n")
            
            self.gettime()
        else:
            pass
        
    def isadmin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def request(self):
        if self.SSL:
            pass
        else:
            urllib3.disable_warnings()

        response = requests.get(self.URL, verify=False).content.decode("utf-8").rsplit(" ", 1)

        return response[0], response[1]

    def gettime(self):
        date, time = self.request()
        
        filter_date, filter_time = date.rsplit("/", 3), time.rsplit(":", 2)
            
        self.date["day"], self.date["month"], self.date["year"] = int(filter_date[0]), int(filter_date[1]), int(filter_date[2])
        self.time["hour"], self.time["minute"], self.time["second"] = int(filter_time[0]), int(filter_time[1]), int(filter_time[2])

        day = Timestamp(f"{self.date['year']}-{filter_date[1]}-{self.date['day']}")

        print(f"({self.URL}): {self.date['day']}/{filter_date[1]}/{self.date['year']} - | {day.day_name()} | - {self.time['hour']}:{self.time['minute']}:{self.time['second']}")

        realtime = datetime.strptime(f"{self.date['year']} {filter_date[1]} {self.date['day']} {self.time['hour']} {self.time['minute']} {self.time['second']} {self.time['millseconds']}", "%Y %m %d %H %M %S %f")

        self.settime(realtime)
        
    def settime(self, datetime_obj: datetime):
        time.sleep(1.5)
        
        if self.isadmin():        
            utc_datetime = datetime_obj.astimezone().astimezone(timezone.utc).replace(tzinfo=None)
            day_of_week = utc_datetime.isocalendar()[2]
            win32api.SetSystemTime(utc_datetime.year, utc_datetime.month, day_of_week, utc_datetime.day, utc_datetime.hour, utc_datetime.minute, utc_datetime.second, int(utc_datetime.microsecond / 1000))
        
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        
app = correct_datetime()

