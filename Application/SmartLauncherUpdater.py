import urllib, os, traceback

from github import Github
from cryptography.fernet import Fernet

class ApplicationUpdate:
    def __init__(self):
        self.token = "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"
        self.repository = "RIick-013/SmartLauncher"

        self.account = Github(self.token)

        self.fernet = Fernet(Fernet.generate_key())
    
    def encrpyt(self, data):
        return self.fernet.encrypt(data.encode())

    def decrypt(self, data):
        return self.fernet.decrypt(data).decode()

    def get_repo(self):
        return self.account.get_repo(self.repository)

    def download(self):
        try:
            latest = self.get_repo().get_latest_release()
            asset = self.get_repo().get_latest_release().get_assets()[0]
            
            path = os.path.exists("./data/update.data")
            if path:
                data = latest.title

                print(data)
            else:
                print("no")
            
            
        except:
            print(f"{traceback.format_exc()}")

x = ApplicationUpdate().download()