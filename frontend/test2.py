import ctypes
import sys

from ctypes import wintypes

user32 = ctypes.WinDLL("user32")

SW_HIDE = 0
SW_SHOW = 5

HIDE = True;

for idx,item in enumerate(sys.argv):
    print(idx, item);
    if (idx == 1 and item.upper() == 'SHOW'):
        HIDE = False;

#HIDE = sys.argv[1] = 'HIDE' ? True : False;


user32.FindWindowW.restype = wintypes.HWND
user32.FindWindowW.argtypes = (
    wintypes.LPCWSTR, # lpClassName
    wintypes.LPCWSTR) # lpWindowName

user32.ShowWindow.argtypes = (
    wintypes.HWND, # hWnd
    ctypes.c_int)  # nCmdShow

def hide_taskbar():
    hWnd = user32.FindWindowW(u"Shell_traywnd", None)
    user32.ShowWindow(hWnd, SW_HIDE)

    hWnd_btn_start = user32.FindWindowW(u"Button", 'Start')
    user32.ShowWindow(hWnd_btn_start, SW_HIDE)

def unhide_taskbar():
    hWnd = user32.FindWindowW(u"Shell_traywnd", None)
    user32.ShowWindow(hWnd, SW_SHOW)

if (HIDE):
    hide_taskbar();
else:
    unhide_taskbar();
