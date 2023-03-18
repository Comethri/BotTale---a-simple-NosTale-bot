import tkinter as tk
import win32gui
import win32con
import ctypes


PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_READ = 0x00000010

address = 0x15D8E6F4
window_title = "NosTale"

# Finden des Fensters
hwnd = ctypes.windll.user32.FindWindowW(None, window_title)
if hwnd == 0:
    print("NosTale is not open")
    exit()

# Finden der Prozess-ID des Fensters
pid = ctypes.c_ulong()
ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

# Öffnen des Prozesses
process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
if process_handle == 0:
    print("cant open the process, maybe NosTale is not open?")
    exit()

# Auslesen des Werts an der Adresse
value = ctypes.c_ulong()
ctypes.windll.kernel32.ReadProcessMemory(process_handle, address, ctypes.byref(value), ctypes.sizeof(value), None)

# Schließen des Prozesses
ctypes.windll.kernel32.CloseHandle(process_handle)

label_text2 = "HP" , value.value


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
root.resizable(False, False)  # Das Fenster ist nicht resizeable

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

root.mainloop()
