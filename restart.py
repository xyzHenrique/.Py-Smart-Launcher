from modules.logger import ApplicationLogger

import os

class ApplicationRestart:
    def __init__(self):
        pass
    
    def restart(self):
        try: 
            self.register.write(["CRITICAL", f"reiniciando aplicação, aguarde.\n"])

            os.system("taskkill /F /IM chrome* /T >nul 2>&1")

            time.sleep(0.5)

            with open("./system/session", "r") as file:
                line = file.readline()
                os.system(f"start {line}")
            
            os._exit(0)

        except Exception as err:
            self.register.write(["ERROR", f"{err}"])
                
            os._exit(0)