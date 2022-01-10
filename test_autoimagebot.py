import pyautogui

icon_pos = pyautogui.locateOnScreen('system/images/restore.png')

if icon_pos:
    print(icon_pos)
    print("Existe um cadeado aberto na tela")
else:
    print("Não existe nenhum cadeado aberto na tela")