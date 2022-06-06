import json

class Themes:
    def __init__(self):
        self.modules = {
            "canvas": "",
            "topbar": "",
            "sidebar": "",
            "bottombar": "",
            }

    def load_theme(self):
        file = open("./themes/modern.json")

        data = json.load(file)

        print(data["canvas"])

        self.modules["canvas"] = data["canvas"]["main-color"]
        self.modules["topbar"] = data["canvas"]["topbar-color"]
        self.modules["sidebar"] = data["canvas"]["sidebar-color"]
        self.modules["bottombar"] = data["canvas"]["bottombar-color"]
        
        file.close()

        return self.modules
        
        