import pyautogui
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

icon_pos = pyautogui.locateOnScreen('system/images/minidb/restore_1.png')

if icon_pos:
    print(icon_pos)
    print("yes, exists")
    pyautogui.moveTo(icon_pos)
    pyautogui.click()
else:
    print("no, exists")
