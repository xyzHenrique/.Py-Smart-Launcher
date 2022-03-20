import datetime, os

class ApplicationLogger:
    def __init__(self):
        self.filename = self.custom_date("%m-%Y")
        self.foldername = self.custom_date("%d/%m/%Y") + "-" + self.custom_time("%H-%M")
        
        self.folderlogs = "logs/"

    def custom_date(self, date_format):
        self.date = datetime.datetime.today().strftime(date_format)

        return self.date
        
    def custom_time(self, time_format):
        self.time = datetime.datetime.now().strftime(time_format)

        return self.time

    def create_folder(self):
        if not os.path.exists(f"{self.folderlogs}{self.foldername}"):
            os.mkdir(f"{self.folderlogs}{self.foldername}")

            self.create_file()
        else:
            self.create_file()

    def create_file(self):
        file = open(f"{self.folderlogs}{self.filename}/{self.filename}", "a")

        file.write("teste\n")

ApplicationLogger().create_folder()