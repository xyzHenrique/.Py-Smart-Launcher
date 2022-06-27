"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

path: ApplicationLogger.py
version: 5.0.0
"""

### NATIVE
import os, json, time, datetime, platform, re, uuid, shutil, zipfile

### THIRD
import colorama

### LOCAL 
from ApplicationInformation import Informations

class Logger:
    def __init__(self):
        ### CALL and INITIALIZE THIRD PACKAGE
        colorama.init()

        ### CALL and INITIALIZE LOCAL PACKAGE
        self.structure = json.load(open("Structure"))

        ### ... ###
        self.filename_format = "%d-%m"
        self.foldername_format = "%m-%Y" 

        self.file = {
            "file": None,
            "filename": self.GetDate(self.filename_format),
            "extension": ".txt"
        }

        self.folder = {
            "foldername": self.GetDate(self.foldername_format),
            "folderpath": self.structure["Application.Logs"]["dir"]
        }

        self.current_datetime = {
            "date": self.GetTime("%d/%m/%Y"),
            "time": self.GetDate("%H:%M:%S")
        }

        self.fullpath = f"{self.folder['folderpath']}/{self.folder['foldername']}/{self.file['filename']}{self.file['extension']}"

    def GetDate(self, date_format):
        self.date = datetime.datetime.today().strftime(date_format)

        return self.date
        
    def GetTime(self, time_format):
        self.time = datetime.datetime.now().strftime(time_format)

        return self.time

    def InitializeLogger(self):
        def Header():
            self.file["file"] = open(self.fullpath, "w")
            self.file["file"].write(f"""------------------------------------------------------------------------
Logging started at {self.current_datetime['date']} - {self.current_datetime['time']}
File                 : {self.file['filename']}
Version              : {Informations['APP_VERSION']}
Computer             : Name: {platform.node()} || Mac: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}
------------------------------------------------------------------------\n""")
            self.file["file"].close()  
        
        if os.path.exists(f"{self.folder['folderpath']}/{self.folder['foldername']}"):
            if os.path.exists(self.fullpath):
                self.CompactFolder()
            else:
                Header()
            
                self.CompactFolder()
        else:
            try:
                os.mkdir(f"{self.folder['folderpath']}/{self.folder['foldername']}")

                Header()

                self.CompactFolder()

            except Exception as err:
                print(err)

    def CompactFolder(self):
        for dir in os.listdir(self.folder["folderpath"]):
            if not dir == self.GetDate(self.foldername_format) and not os.path.splitext(dir)[1] == ".zip":
                zip_file = zipfile.ZipFile(f"{self.folder['folderpath']}/{dir}.zip", 'w', zipfile.ZIP_DEFLATED)

                for root, dirs, files in os.walk(f"{self.folder['folderpath']}/{dir}"):
                    for file in files:
                        zip_file.write(os.path.join(root, file))
                zip_file.close()

                shutil.rmtree(f"{self.folder['folderpath']}/{dir}")
        
    def WriteFile(self, message: str, level=list(["INFO", "WARNING", "CRITICAL", "DEBUG"])):
        if os.path.exists(self.fullpath):
            self.file["file"] = open(self.fullpath, "a")

            if level == "INFO":
                self.file["file"].write(f"[{self.current_datetime['time']}]: {level} - {message}\n")
                
                print(colorama.Fore.CYAN + f"[{self.current_datetime['time']}]: {level} - {message}\n")
                print(colorama.Fore.RESET)
                
                self.file['file'].close()

            elif level == "WARNING":
                self.file["file"].write(f"[{self.current_datetime['time']}]: {level} - {message}\n")
                
                print(colorama.Fore.YELLOW + f"[{self.current_datetime['time']}]: {level} - {message}\n")
                print(colorama.Fore.RESET)
                
                self.file["file"].close()
            
            elif level == "CRITICAL":
                self.file["file"].write(f"[{self.current_datetime['time']}]: {level} - {message}\n")
                
                print(colorama.Fore.RED + f"[{self.current_datetime['time']}]: {level} - {message}\n")
                print(colorama.Fore.RESET)
                
                self.file["file"].close()

            elif level == "DEBUG":
                self.file["file"].write(f"[{self.current_datetime['time']}]: {level} - {message}\n")
                
                print(colorama.Fore.MAGENTA + f"[{self.current_datetime['time']}]: {level} - {message}\n")
                print(colorama.Fore.RESET)
                
                self.file["file"].close()