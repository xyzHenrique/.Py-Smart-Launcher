import tkinter as tk

from glob import glob
from turtle import color
from PIL import Image, ImageTk
from numpy import pad

class ApplicationConfiguration:
    def __init__(self):
        self.app = tk.Tk() 

        self.app.geometry("540x320")
        self.app.title("...")

        self.menubar_module()
        self.preset_page_module()

        self.app.mainloop()
    
    def add_preset(self, monitors_total, description, enabled, pos_x, pos_y, size_enabled, size_x, size_y, dir):
        preset_base = """
        {
            'MONITORS': {
                '{}': {
                    'PROPERTIES': {
                        '.DESCRIPTION': '{}',
                        '.ENABLED': {},
                        '.X': {},
                        '.Y': {},
                    
                        'SIZE': {
                            '.ENABLED': {}, 
                            '.X': {},
                            '.Y': {} 
                        },

                        'DIR': '{}'
                    }
                }
            }
        }
        """.format(monitors_total, description, enabled, pos_x, pos_y, size_enabled, size_x, size_y, dir)

    def get_presets(self):
        folders = glob("./system/presets/*", recursive = True)

        print(folders)

        folders = tk.StringVar(value=folders)

        return folders

    def menubar_module(self):
        self.menubar = tk.Menu(self.app)

        menubar_home_icon = Image.open("./system/images/icons/GUI_home_icon.png")
        menubar_home_icon = menubar_home_icon.resize((25, 25), Image.ANTIALIAS)
        menubar_home_icon = ImageTk.PhotoImage(menubar_home_icon)

        menubar_preset_icon = Image.open("./system/images/icons/GUI_preset_icon.png")
        menubar_preset_icon = menubar_preset_icon.resize((25, 25), Image.ANTIALIAS)
        menubar_preset_icon = ImageTk.PhotoImage(menubar_preset_icon)

        homemenu_btn = tk.Button(self.menubar)
        presetmenu_btn = tk.Button(self.menubar)
        
        self.menubar.add_cascade(label="Home", menu=homemenu_btn)
        self.menubar.add_cascade(label="Presets", menu=presetmenu_btn)

        self.app.config(menu=self.menubar)
    
    def preset_page_module(self):
        
        ### preset list
        l1 = tk.Label(self.app, text="PRESETS")
        l1.config(font=("Arial", 9))
        l1.pack(padx=1, pady=0)
        

        listbox = tk.Listbox(self.app, listvariable=self.get_presets(), selectmode='browse')
        listbox.config(height=5, width=18)

        listbox.pack(padx=50, pady=50)

ApplicationConfiguration()


