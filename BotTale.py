import tkinter as tk
import win32gui
import win32con
import pymem
import pymem.process

window_title = "NosTale"
pm = pymem.Pymem("NosTaleClientX.exe")

# get the base address of the game module
gameModule = pymem.process.module_from_name(pm.process_handle, "NosTaleClientX.exe").lpBaseOfDll

def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i !=offsets[-1]:
            addr = pm.read_int(addr + i)
        else:
            addr += i
    return addr

HP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x4C])
valueHP = pm.read_int(HP_address)
label_text2 = valueHP

MP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0x4C])
valueMP = pm.read_int(MP_address)
label_text3 = valueMP

# leertasten bot
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


# Main Window
root = tk.Tk()
root.title("BotTale")
root.resizable(False, False)

hwnd = win32gui.FindWindow(None, "NosTale")
if hwnd == 0:
    label_text = "can't find NosTale"
else:
    label_text = "NosTale found"

canvas = tk.Canvas(root, bg="#263D42")
canvas.grid(columnspan=2, rowspan=2)

button1 = tk.Button(root, text="Start", command=button1_click, bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click, bg="white", fg="black", width=10)
button2.grid(column=1, row=0)

label1 = tk.Label(root, text=label_text, bg="#263D42", fg="white")
label1.grid(column=0, row=1)

label2 = tk.Label(root, text=label_text2, bg="#263D42", fg="white")
label2.grid(column=1, row=1)

label2 = tk.Label(root, text=label_text3, bg="#263D42", fg="white")
label2.grid(column=2, row=1)

root.mainloop()
