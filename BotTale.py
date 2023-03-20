import tkinter as tk
import win32gui
import win32con
import pymem
import pymem.process

window_title = "NosTale"
pm = pymem.Pymem("NosTaleClientX.exe")
gameModule = pymem.process.module_from_name(pm.process_handle, "NosTaleClientX.exe").lpBaseOfDll

try:
    process = pymem.Pymem("NosTaleClientX.exe")
    find = "NosTale found"
except pymem.exception.ProcessNotFound:
    find = "nosTale not found"



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
targetHP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0xC4])
targetMP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x22C])
xP_address = GetPtrAddr(gameModule + 0x004B324C, [0x158])
lvl_address = GetPtrAddr(gameModule + 0x004B313C, [0x80])

def update_values():
    global valueHP, valueMP, valueTargetHP, valueTargetMP, valueXP, valueLvl
    valueHP = pm.read_int(HP_address)
    valueMP = pm.read_int(MP_address)
    valueTargetHP = pm.read_int(targetHP_address)
    valueTargetMP = pm.read_int(targetMP_address)
    valueXP = pm.read_int(xP_address)
    valueLvl = pm.read_int(lvl_address)
    label_text2 = "HP:" + str(valueHP)
    label_text3 = "MP:" + str(valueMP)
    label_text4 = "HP:" + str(valueTargetHP)
    label_text5 = "MP:" + str(valueTargetMP)
    label_text6 = "XP:" + str(valueXP)
    label_text7 = "LV:" + str(valueLvl)
    label2.config(text=label_text2)
    label3.config(text=label_text3)
    label4.config(text=label_text4)
    label5.config(text=label_text5)
    label6.config(text=label_text6)
    label7.config(text=label_text7)
    root.after(1000, update_values)


# Leertasten bot via keypress
bot_running = False

def button1_click():
    global bot_running
    global status
    bot_running = True
    perform_spacebar()
    status = "Started"
    label0.config(text=status)

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
    status = "Stopped"
    label0.config(text=status)

#window that opens when you start the program
root = tk.Tk()
root.title("BotTale")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="#263D42")

button1 = tk.Button(root, text="Start", command=button1_click, bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click, bg="white", fg="black", width=10)
button2.grid(column=0, row=1)

status = "Not started"
label0 = tk.Label(root, text=status)
label0.grid(column=0, row=2, sticky="W")

label1 = tk.Label(root, text=find)
label1.grid(column=0, row=3, sticky="W")

#player label
player = tk.Label(root, text="Player")
player.grid(column=2, row=0, sticky="W")

label2 = tk.Label(root)
label2.grid(column=2, row=1, sticky="W")

label3 = tk.Label(root)
label3.grid(column=2, row=2, sticky="W")

label6 = tk.Label(root)
label6.grid(column=2, row=3, sticky="W")

label7 = tk.Label(root)
label7.grid(column=2, row=4, sticky="W")

input0 = tk.Entry(root)
input0.grid(column=3, row=1, sticky="W")

#target label
target = tk.Label(root, text="Target")
target.grid(column=4, row=0, sticky="W")

label4 = tk.Label(root)
label4.grid(column=4, row=1, sticky="W")

label5 = tk.Label(root)
label5.grid(column=4, row=2, sticky="W")

update_values()

root.mainloop()