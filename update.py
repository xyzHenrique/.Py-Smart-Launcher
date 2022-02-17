# ----------------------------------------------------------------------------------------------
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
# ----------------------------------------------------------------------------------------------

""" API: https://chromedriver.storage.googleapis.com/index.html """

from modules.logger import ApplicationLogger

from uuid import uuid4

import requests, zipfile, time, os 

class ApplicationUpdate:
    def __init__(self):
        self.NAME = uuid4().hex
        self.CACHE = "./cache/"
        self.OUTPUT = "./driver/"
        self.VERSION = "./version"
         
        if not os.path.exists(self.CACHE):
            os.makedirs(self.CACHE)
        
    def clean_cache(self):
        time.sleep(1.5)

        arr = os.listdir(self.CACHE)

        if len(arr) >= 1:
            for item in arr:
                os.remove(f"{self.CACHE}{item}")
        else:
            pass

    def check_version(self):
        r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        f = open(self.VERSION, "r")

        c_v = f.read()
        l_v = r.content.decode("utf-8")

        __c_v = c_v[:3].replace(".", "")
        __l_v = l_v[:3].replace(".", "")

        if __c_v == __l_v:
            return False, [c_v, l_v]
        else: 
            return True, [c_v, l_v]

    def download(self, l_v):
        self.clean_cache()

        with open(f"{self.CACHE}{self.NAME}.zip", "wb") as f:
            r = requests.get(f"https://chromedriver.storage.googleapis.com/{l_v}/chromedriver_win32.zip")

            with open(f"{self.CACHE}{self.NAME}.zip", "wb") as f:
                f.write(r.content)
                f.close()

                self.install(f.name, l_v)
            
    def install(self, name, l_v):
        try:
            with open(name, "rb") as f:
                z = zipfile.ZipFile(f)
                z.extractall(self.OUTPUT)
                z.close()

                print(f"atualização: ({l_v}) instalada com sucesso!")
            
            f = open(f"{self.VERSION}", "w")
            f.write(l_v)
            f.close()

        except Exception as err:
            print(f"atualização: ({l_v}) não instalada!\n{err}")

app = ApplicationUpdate()