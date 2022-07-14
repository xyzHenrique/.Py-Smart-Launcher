from tkinter import font, scrolledtext, ttk
import psutil, threading, time

from tkinter import *
from PIL import Image, ImageTk

from themes.theme import Themes

class UI:
    def __init__(self):
        self.themes = Themes().load_theme()

        self.root = Tk()

        self.window_width = 1024
        self.window_height = 550

        self.hardware = {"THREAD": True, "CPU": "", "RAM": ""}
        self.status = {"THREAD": True, "STATUS": "OFFLINE"}

        self.sidebar_width = self.window_width/2
        self.sidebar_expanded = False

        self.configuration()
        self.build()

    def configuration(self):
        self.root.title("FoxWebLauncher - Dashboard")

        self.root.resizable(False, False)
        
        wW = self.root.winfo_reqwidth()
        wH = self.root.winfo_reqheight()
        
        posR = int(self.root.winfo_screenwidth()/5.5 - wW/2)
        posD = int(self.root.winfo_screenheight()/3 - wH/2)

        self.root.geometry("+{}+{}".format(posR, posD))

    def layout(self):
        def _create_circle(self, x, y, r, **kwargs):
            return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        
        Canvas.create_circle = _create_circle

        self.main_canvas = Canvas(self.root, width=self.window_width, height=self.window_height, borderwidth=0, highlightthickness=0, background=self.themes["canvas"], relief="raised")
        self.main_canvas.pack(padx=0, pady=0)

        self.topbar_position = [0, 0, self.window_width, 15]
        self.bottombar_position = [self.window_width, self.window_height, 0, self.window_height-27]
        self.sidebar_position = [65, self.topbar_position[3]-0.3, 0, self.bottombar_position[3]-0.3]
        
        self.topbar = self.main_canvas.create_rectangle(self.topbar_position[0], self.topbar_position[1], self.topbar_position[2], self.topbar_position[3], fill=self.themes["topbar"], outline="")
        self.sidebar = self.main_canvas.create_rectangle(self.sidebar_position[0], self.sidebar_position[1], self.sidebar_position[2], self.sidebar_position[3], fill=self.themes["sidebar"], outline="")
        self.bottombar = self.main_canvas.create_rectangle(self.bottombar_position[0], self.bottombar_position[1], self.bottombar_position[2], self.bottombar_position[3], fill=self.themes["bottombar"], outline="")

    
    def scrolled_text(self):
        def ctrl(event):
            if (12==event.state and event.keysym=="c"):
                return
            else:
                return "break"

        scrolledarea = scrolledtext.ScrolledText(self.main_canvas, wrap = WORD, font=("Halvetica", 10))
        scrolledarea.config(background="#ededed")
        
        y = [". . ."]

        count = 0
        for x in y[count:]:  
            scrolledarea.insert(END, str(x) + "\n")
            scrolledarea.yview(END)

            count += 1
            
        text_area_window = self.main_canvas.create_window(self.sidebar_position[1]+59, self.topbar_position[3]+1, width=720, height=int(self.bottombar_position[3]-25), anchor=NW, window=scrolledarea)
        
        scrolledarea.bind("<Key>", lambda e: ctrl(e))

    def build_buttons(self):
        self.button1 = Button(self.main_canvas, text = "demo", command = print("a"), anchor=W)
        self.button1.configure(width=10, activebackground="gray", bg="black", fg="black", relief=RIDGE)
        
        self.button1_window = self.main_canvas.create_window(0, 3, width=50, height=15, anchor=NW, window=self.button1)

    def status_update(self):
        while self.status["THREAD"]:
            if self.status["STATUS"] == "CONNECTED":
                self.bottom_text_1 = self.main_canvas.create_text(50, self.window_height-13, text="ONLINE", fill="white", font=("Arial", "9", "bold"))
                self.bottom_circ_1 = self.main_canvas.create_circle(15, self.bottombar_position[3]+13, 5, fill="green", outline="", width=1)
            elif self.status["STATUS"] == "CONNECTING":
                self.bottom_text_1 = self.main_canvas.create_text(63, self.window_height-13, text="CONNECTING", fill="white", font=("Arial", "9", "bold"))
                self.bottom_circ_1 = self.main_canvas.create_circle(15, self.bottombar_position[3]+13, 5, fill="orange", outline="", width=1)
            else:
                self.bottom_text_1 = self.main_canvas.create_text(50, self.bottombar_position[3]+13, text="OFFLINE", fill="white", font=("Arial", "9", "bold"))
                self.bottom_circ_1 = self.main_canvas.create_circle(15, self.window_height-13, 5, fill="red", outline="", width=1)

            time.sleep(1.5)

            self.main_canvas.delete(self.bottom_text_1)
            self.main_canvas.delete(self.bottom_circ_1)

    def harware_update(self):
        while self.hardware["THREAD"]:
            self.bottom_text_2 = self.main_canvas.create_text(self.window_width-50, self.bottombar_position[3]+13, text=f"CPU: {self.hardware['CPU']}%", fill="white", font=("Arial", "9", "bold"))
            self.bottom_text_3 = self.main_canvas.create_text(self.window_width-130, self.bottombar_position[3]+13, text=f"RAM: {self.hardware['RAM']}%", fill="white", font=("Arial", "9", "bold"))
            
            time.sleep(1.5)

            self.hardware["CPU"] = psutil.cpu_percent()
            self.hardware["RAM"] = psutil.virtual_memory().percent

            self.main_canvas.delete(self.bottom_text_2)
            self.main_canvas.delete(self.bottom_text_3)

    def build(self):
        self.layout()
        self.scrolled_text()

        threading.Thread(target=self.harware_update, daemon=True).start()
        threading.Thread(target=self.status_update, daemon=True).start()

        self.root.mainloop()

app = UI()
