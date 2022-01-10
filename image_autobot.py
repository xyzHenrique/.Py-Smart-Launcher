import pyautogui
from PIL import ImageGrab
import glob
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

for file in glob.glob("./system/images/minidb/*.png"):
    img = pyautogui.locateOnScreen(file)

    if img:
        print(img)
        print("yes")
        
        pyautogui.moveTo(img)
        pyautogui.click()
    else:
        print("no")