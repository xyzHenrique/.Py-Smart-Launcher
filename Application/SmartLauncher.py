"""
created by: Henrique Rodrigues Pereira <https://github.com/RIick-013>

--LINKS--
 https://chromedriver.storage.googleapis.com/index.html 

SmartLauncher
"""

import sys


try:
    ### NATIVE
    import os, time, json, threading, traceback, pathlib
    
    ### THIRD
    import pyautogui, keyboard

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    
    ### LOCAL
    from ApplicationInformation import Informations
    from ApplicationLogger import Logger
    from ApplicationScreenController import ScreenController
    from ApplicationSettings import AutomationSettings, SystemSettings
    from ApplicationStructure import Structure

except ImportError:
    print(ImportError)

class Application:
    def __init__(self):
        ### CALL and INITIALIZE LOCAL PACKAGE
        self.structure = json.load(open("Structure"))

        self.logger = Logger()
        self.screen_controller = ScreenController()
        self.automation_settings = AutomationSettings()
        self.system_settings = SystemSettings()

        self.logger.InitializeLogger()
        
        ### ...
        self.preset = json.load(open(f"{self.structure['Application.Presets']['dir']}/{self.system_settings['Preset']['Set']}/preset.json"))
        
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
        
        print(f"{Informations['APP_NAME']} - ({Informations['APP_VERSION']}) - created by: {Informations['APP_OWNER']}")

        ### FUNCTIONS
        ###self.secure_start()
        self.MonitorSetup()
    
    def CreateThread(self, target, args, daemon):
        thread = threading.Thread(target=target, args=args, daemon=daemon).start()

        self.threads.append[thread]
        
    def secure_start(self):
        if self.settings_general_system["secure-start"]:
            self.module_chrome_controller.end(onlychrome=True)

    def secure_exit(self):
        while self.settings_general_system["secure-exit"]["enabled"]:
            if keyboard.is_pressed(f"{self.settings_general_system['secure-exit']['keys']}"):
                self.module_logger.write_file(["INFO", f"({self.settings_general_system['secure-exit']['keys']}) closing application, please wait..."])

                self.module_chrome_controller.end(onlychrome=False)
                           
    def automation(self):
        enabled = self.settings_general_automation["automation"]["enabled"]
        timer_enabled = self.settings_general_automation["timer"]["enabled"]
        timer_time = self.settings_general_automation["timer"]["time"]
        show = self.settings_general_automation["show"]
        keys = self.settings_general_automation["keys"]
        
        if enabled:
            pyautogui.press("enter")
            try:
                for key in keys:
                    pyautogui.press(key)

                    if show:
                        self.module_logger.write_file(["DEBUG", f"{key} pressed!"])
                    if timer_enabled:
                        time.sleep(timer_time)

            except Exception:
                self.module_logger.write_file(["ERROR", f"{traceback.format_exc()}"])

    def MonitorEngine(self, name):
        try:
            for monitor in self.monitors.keys():
                if name == monitor:
                    driver = self.monitors[name]["MonitorDriver"]
                    driver.get(self.monitors[name]["MonitorURL"])

                    ### self.automation()

                    driver.execute_script("window.focus()")
                    driver.execute_script(f'document.title = "monitor {name} - ({driver.service.process.pid})"')

                    self.logger.WriteFile(f"Monitor {name} || PID: {driver.service.process.pid} OK!", "INFO")
                    self.module_logger.write_file(["INFO", f"monitor {self.monitors[name]['monitor_name']} ({self.monitors[name]['monitor_PID']}) OK!"])

                    i = 0
                    while True:
                        if self.settings_general_dev["enabled"]:
                            driver.execute_script(f'document.title = "DEV - {name} - ({driver.service.process.pid})"')

                            if keyboard.is_pressed(self.settings_general_dev["keys"]):
                                driver.get(self.settings_general_dev["url"])
                        else:
                            if block_enabled:
                                for blocked in block_url:
                                    if driver.current_url == blocked or not driver.current_url == application_url:
                                        i += 1

                                        self.module_logger.write_file(["WARNING", f"Invalid URL running on monitor: ({name}) - ({driver.current_url}), corrections: ({i})"])
                                        
                                        driver.get(application_url)
                                        driver.execute_script(f'document.title = "monitor {name} - ({driver.service.process.pid})"')
                                    
                                        print(i)
                                    
                                    if i >= 3:
                                        self.module_logger.write_file(["WARNING", f"the maximum number of correction attempts has been reached!"])
                                            
                                        driver.quit()

                                        self.module_chrome_controller.restart()

        except Exception:
            self.module_logger.write_file(["WARNING", f"monitor {self.monitors[name]['monitor_name']} ({traceback.format_exc()})"])
            self.module_chrome_controller.restart()
        
    def MonitorSetup(self):
        try:
            for monitor in self.monitors.values():
                if monitor["MonitorEnabled"]: 
                    driver = webdriver.ChromeOptions()

                    """1"""
                    driver.add_experimental_option("useAutomationExtension", False)
                    driver.add_experimental_option("excludeSwitches",["enable-automation", "enable-logging"])

                    """2"""
                    if "~*local" in monitor["MonitorPath"]:
                        path = monitor["MonitorPath"].replace("~*local", os.getcwd())
                        
                        driver.add_argument(f"--user-data-dir={path}")
                    else:
                        driver.add_argument(f"--user-data-dir={monitor['MonitorPath']}")
                    
                    driver.add_argument(f"--window-position={monitor['MonitorWidth']},{monitor['MonitorHeight']}")

                    """3"""
                    if monitor["MonitorCustomSizeEnabled"]:
                        driver.add_argument(f"--app={monitor['MonitorURL']}")
                        driver.add_argument(f"--window-size={monitor['MonitorCustomSizeWidth']},{monitor['MonitorCustomSizeHeight']}")
                    else:
                        driver.add_argument("--kiosk")
                    
                    """4"""
                    for argument in self.system_settings["Engine"]["BasicArguments"]:
                        driver.add_argument(argument)
                              
                    """5"""
                    try:
                        """ONLINE STARTUP"""
                        monitor["MonitorDriver"] = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver)
                       
                    except:
                        self.logger.WriteFile(f"{traceback.format_exc()}", "WARNING")

                        """OFFLINE STARTUP"""
                        file = f"{os.path.expanduser('~')}\.wdm\drivers\chromedriver\win32\{self.driver_version}\chromedriver.exe"

                        if pathlib.Path(file):
                            monitor["MonitorDriver"] = webdriver.Chrome(executable_path=file, options=driver)
                        else:
                            self.logger.WriteFile(f"{traceback.format_exc()}", "CRITICAL")

                            ### self.module_chrome_controller.restart() 

                    print(driver)
                    #self.CreateThread(self.)
                    #thread = threading.Thread(target=self.monitor_manager, args=(monitor["monitor_name"]))
                    #monitor["monitor_thread"] = thread  
                    #thread.start()
                
                else:
                    self.logger.WriteFile(f"Monitor {monitor['MonitorName']} disabled!", "WARNING")
        
        except Exception:
            self.logger.WriteFile(f"{traceback.format_exc()}", "CRITICAL")

            #### self.module_chrome_controller.end(onlychrome=False)

Application()
