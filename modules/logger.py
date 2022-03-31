"""
created by: Henrique R. Pereira <https://github.com/RIick-013>

modules > logger.py | v2 |
"""

import datetime, os

class ApplicationLogger:
    def __init__(self):
        self.file = None
        self.filename = self.custom_date("%d-%m")
        self.foldername = self.custom_date("%m-%Y")        
        self.folderpath = "./logs/"

        self.normal_datetime = [self.custom_date("%d/%m/%Y"), self.custom_time("%H:%M:%S")]

        self.create_folder()

    def custom_date(self, date_format):
        self.date = datetime.datetime.today().strftime(date_format)

        return self.date
        
    def custom_time(self, time_format):
        self.time = datetime.datetime.now().strftime(time_format)

        return self.time

    def create_folder(self):
        if os.path.exists(f"{self.folderpath}{self.foldername}"):
            self.first_write()
        else:
            try:
                os.mkdir(f"{self.folderpath}{self.foldername}")

                self.first_write()

            except Exception as err:
                print(err)

    def first_write(self):
        self.file = open(f"{self.folderpath}{self.foldername}/{self.filename}.txt", "w")

        self.file.write(f"\n------------ LOG FILE | {self.normal_datetime[0]} - {self.normal_datetime[1]} ------------\n")

        self.file.close()

    def write_file(self, content):
        if os.path.exists(f"{self.folderpath}{self.foldername}/{self.filename}.txt"):
            self.file = open(f"{self.folderpath}{self.foldername}/{self.filename}.txt", "w")
            
            self.file.write(f"[{self.normal_datetime[1]}] - {content[0]} - {content[1]}\n")        
            
            print(f"[{self.normal_datetime[1]}] - {content[0]} - {content[1]}\n")

            self.file.close()
        else:
            self.create_folder()            
        
