"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

--LINKS--
 https://chromedriver.storage.googleapis.com/index.html 

SmartLauncher
"""

try:
    ### NATIVE
    import os, time, json, threading, traceback 
    
    ### THIRD
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    ### from webdriver_manager.chrome import ChromeDriverManager ###
    
    ### LOCAL
    from ApplicationScreenController import ScreenController
    from ApplicationInformation import Informations
    from ApplicationStructure import Structure
    from ApplicationSettings import AutomationSettings, SystemSettings
    from ApplicationLogger import Logger

except ImportError:
    print(ImportError)

class Application:
    def __init__(self):
        ### CALL and INITIALIZE LOCAL PACKAGE
        self.structure = json.load(open("Structure"))

        self.application_screen_controller = ScreenController()
        self.application_structure = Structure()
        self.application_logger = Logger()
       
        self.application_automation_settings = AutomationSettings()
        self.application_system_settings = SystemSettings()

        self.application_structure.CheckFileStructure()
        self.application_structure.CheckFolderStructure()
        
        self.application_logger.InitializeLogger()

        ### ...
        self.preset = json.load(open(f"{self.structure['Application.Presets']['dir']}/{self.application_system_settings['Preset']['Set']}/preset.json"))
        
        self.monitors = dict()
        self.threads = list()

        for key,item in self.preset.items():
            self.monitors[key] = {
                "MonitorName": key,
                "MonitorDriver": None,
                "MonitorPID": None,

                "MonitorEnabled": item["Enabled"],
                "MonitorURL": item["URL"],
                "MonitorPath": item["Path"],
                "MonitorWidth": item["Width"],
                "MonitorHeight": item["Height"],
                
                "MonitorCustomSizeEnabled": item["CustomSize"]["Enabled"],
                "MonitorCustomSizeWidth": item["CustomSize"]["Width"],
                "MonitorCustomSizeHeight": item["CustomSize"]["Height"],

                "Description": item["Description"],
            }
        
        print(f"{Informations['APP_NAME']} - ({Informations['APP_VERSION']}) - created by: {Informations['APP_OWNER']}\n")

        for monitor in self.monitors.values():
            self.CreateSession(monitor)
    
    def CreateSession(self, monitor):
        def Path(path): return path.replace("*~local", os.getcwd())

        try:
            if monitor["MonitorEnabled"]: 
                options = webdriver.ChromeOptions()
            
                ### -------------------------------------------------- ###
                if self.application_system_settings["Engine"]["ChromeBinaryPath"] == "":
                    pass
                elif "*~local" in self.application_system_settings["Engine"]["ChromeBinaryPath"]:
                    options.binary_location = Path(self.application_system_settings["Engine"]["ChromeBinaryPath"])
                else:
                    options.binary_location = self.application_system_settings["Engine"]["ChromeBinaryPath"]
                ### -------------------------------------------------- ###

                ### -------------------------------------------------- ###
                #options.add_experimental_option("detach", True)
                options.add_experimental_option("useAutomationExtension", False)
                options.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])
                ### -------------------------------------------------- ###

                ### -------------------------------------------------- ###
                if "*~local" in monitor["MonitorPath"]:
                    options.add_argument(f"--user-data-dir={Path(monitor['MonitorPath'])}")
                else:
                    options.add_argument(f"--user-data-dir={monitor['MonitorPath']}")
                
                options.add_argument(f"--window-position={monitor['MonitorWidth']},{monitor['MonitorHeight']}")
                ### -------------------------------------------------- ###

                ### -------------------------------------------------- ###
                if monitor["MonitorCustomSizeEnabled"]:
                    options.add_argument(f"--app={monitor['MonitorURL']}")
                    options.add_argument(f"--window-size={monitor['MonitorCustomSizeWidth']},{monitor['MonitorCustomSizeHeight']}")
                else:
                    options.add_argument("--kiosk")
                ### -------------------------------------------------- ###
                
                ### -------------------------------------------------- ###
                for argument in self.application_system_settings["Engine"]["BasicArguments"]:
                    options.add_argument(argument)
                ### -------------------------------------------------- ###
    
                if "*~local" in self.application_system_settings["Engine"]["ChromedriverBinaryPath"]: 
                    driver = webdriver.Chrome(options=options, service=Service(Path(self.application_system_settings["Engine"]["ChromedriverBinaryPath"])))
                    driver.get(monitor["MonitorURL"])
                else:
                    driver = webdriver.Chrome(options=options, service=Service(self.application_system_settings["Engine"]["ChromedriverBinaryPath"]))
                    driver.get(monitor["MonitorURL"])
                
                monitor["MonitorDriver"] = driver
                monitor["MonitorPID"] = driver.service.process.pid
                
                self.threads.append(threading.Thread(target=self.Session, args=(monitor,), daemon=False))
                self.threads[-1].start()
                
            
            else:
                self.application_logger.WriteFile(f"Monitor {monitor['MonitorName']} disabled!", "WARNING")

        except Exception:
            self.application_logger.WriteFile(f"{traceback.format_exc()}", "CRITICAL")

    def Session(self, monitor):
        try:
            name, driver, PID = monitor["MonitorName"], monitor["MonitorDriver"], monitor["MonitorPID"]

            driver.execute_script("window.focus()")
            driver.execute_script(f'document.title = "Monitor ({name}) || PID: ({PID})"')

            self.application_logger.WriteFile(f"Monitor ({name}) || PID: ({PID}) || OK!", "INFO")

            def Monitoring():
                while True:
                    time.sleep(8)
                    
                    block_count = 0
                    
                    for URL in self.application_system_settings["URL"]["Block"]:
                        if driver.current_url == URL:
                            block_count += 1

                            self.application_logger.WriteFile(f"Monitor ({name}) || PID: ({PID}) || URL: ({URL}) is bocked!", "WARNING")

                            driver.get(monitor["MonitorURL"])

                            if block_count >= 3:
                                self.application_logger.WriteFile(f"Monitor ({name}) || PID: ({PID}) || The URL continues to run, the software will restart.", "CRITICAL")
                                driver.close()
            
            Monitoring()                   
        
        except Exception:
            if PID:
                self.application_logger.WriteFile(f"Monitor ({monitor}) || PID: ({PID}) || ({traceback.format_exc()})", "CRITICAL")
            else:
                self.application_logger.WriteFile(f"Monitor ({monitor}) || ({traceback.format_exc()})", "CRITICAL")

Application()