# ----------------------------------------------------------------------------------------------
# Created by: Henrique R. Pereira <https://github.com/RIick-013>
# ----------------------------------------------------------------------------------------------

from urllib import response
from uuid import uuid4

import requests, zipfile, time, os, sys

class ApplicationUpdate:
    def __init__(self):
        self.cache = "./cache/"
        self.version = "./VERSION"
        self.name = str(uuid4().hex)

        if not os.path.exists(self.cache):
            os.makedirs(self.cache)

    def check_version(self):
        r = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        f = open(self.version, "r")

        current_version = f.read()[:3]
        latest_version = r.content.decode("utf-8")[:3]

        __c_v = current_version[:3].replace(".", "")
        __l_v = latest_version[:3].replace(".", "")

        if __c_v == __l_v:
            print(f"'chromedriver.exe' está atualizado: (c-{__c_v} / l-{__l_v})")
  
            return False
        else: 
            print(f"'chromedriver.exe' está desatualizado: (c-{__c_v} / l-{__l_v})")
            
            self.donwload(latest_version)

            return True

    def donwload(self, l_v):
        with open(f"{self.cache}{self.name}.zip", "wb") as f:
            r = requests.get(f"https://chromedriver.storage.googleapis.com/{l_v}/chromedriver_win32.zip", stream=True)

            length = r.headers.get("Content-Length")
            
            if length is None:
                f.write(r.content)

                f.close()
            else:
                fsize = (int(length) / 1024 / 1024)
                print("DOWNLOADING: {0:0.2f} MB".format(fsize))
                progress = 0
                length = int(length)
                for data in r.iter_content(chunk_size=int(length/100)):
                    progress += len(data)
                    f.write(data)
                    
                    done = int(100 * progress / length)
                    
                    sys.stdout.write("\r[%s%s]" % ("#" * done, " " * (100 - done)))
                    sys.stdout.flush()
            
            print(" Complete")

            f.close()
    
            self.install(f.name)
        
        """ WRITE CURRENT VERSION IN VERSION FILE """
        f = open(self.version, "w")
        f.write(str(l_v))

    def install(self, f):
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall(f"./driver")
        os.remove(f)

    def convert_bytes(self, B):
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)

app = ApplicationUpdate()

app.check_version()