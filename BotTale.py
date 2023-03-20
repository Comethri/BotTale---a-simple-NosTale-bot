import tkinter as tk
import win32gui
import win32con
import pymem
import pymem.process

window_title = "NosTale"
pm = pymem.Pymem("NosTaleClientX.exe")
gameModule = pymem.process.module_from_name(pm.process_handle, "NosTaleClientX.exe").lpBaseOfDll


# für die values aus NosTale
def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i !=offsets[-1]:
            addr = pm.read_int(addr + i)
        else:
            addr += i
    return addr

HP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x4C])
MP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0x4C])
enemyHP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0xC4])
enemyMP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x22C])

def update_values():
    global valueHP, valueMP, valueEnemyHP, valueEnemyMP
    valueHP = pm.read_int(HP_address)
    valueMP = pm.read_int(MP_address)
    valueEnemyHP = pm.read_int(enemyHP_address)
    valueEnemyMP = pm.read_int(enemyMP_address)
    label_text2 = "HP:" + str(valueHP)
    label_text3 = "MP:" + str(valueMP)
    label_text4 = "enemy HP:" + str(valueEnemyHP)
    label_text5 = "enemy MP:" + str(valueEnemyMP)
    label2.config(text=label_text2)
    label3.config(text=label_text3)
    label4.config(text=label_text4)
    label5.config(text=label_text5)
    root.after(1000, update_values)

# Leertasten bot via keypress
bot_running = False

def button1_click():
    global bot_running
    bot_running = True
    perform_spacebar()
    print("Bot started")

def perform_spacebar():
    global bot_running
    if bot_running:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd == 0:
            print("can't find NosTale")
        else:
            win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
        root.after(1000, perform_spacebar)

def button2_click():
    global bot_running
    bot_running = False
    print("Bot stopped")


#window that opens when you start the program
root = tk.Tk()
root.title("BotTale")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="#263D42")

button1 = tk.Button(root, text="Start", command=button1_click, bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click, bg="white", fg="black", width=10)
button2.grid(column=0, row=1)

label1 = tk.Label(root, text="NosTale found")
label1.grid(column=2, row=0, sticky="W")

label2 = tk.Label(root, text="HP: ")
label2.grid(column=2, row=1, sticky="W")

label3 = tk.Label(root, text="MP: ")
label3.grid(column=2, row=2, sticky="W")

label4 = tk.Label(root, text="MP: ")
label4.grid(column=2, row=3, sticky="W")

label5 = tk.Label(root, text="MP: ")
label5.grid(column=2, row=4, sticky="W")

update_values()

root.mainloop()