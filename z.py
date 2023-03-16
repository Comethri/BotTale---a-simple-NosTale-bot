import tkinter as tk
import win32gui
import win32con

bot_running = False

def button1_click():
    global bot_running
    bot_running = True
    perform_spacebar()

def perform_spacebar():
    global bot_running
    if bot_running:
        # send spacebar into game with post.message
        hwnd = win32gui.FindWindow(None, "NosTale")
        if hwnd == 0:
            print("can't find NosTale")
        else:
            win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
            win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
        # delay the next spacebar press by 1 second
        root.after(1000, perform_spacebar)

def button2_click():
    global bot_running
    bot_running = False
    print("Bot stopped")

#Main Window
root = tk.Tk()
root.title("BotTale")

hwnd = win32gui.FindWindow(None, "NosTale")
if hwnd == 0:
    label_text = "can't find NosTale"
else:
    label_text = "NosTale found"

canvas = tk.Canvas(root, bg="#263D42")
canvas.grid(columnspan=3, rowspan=3)

button1 = tk.Button(root, text="Start", command=button1_click , bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click , bg="white", fg="black", width=10)
button2.grid(column=0, row=1)

mainText = tk.Label(root, text="this is a\nspacebar bot\nby Comethri\nfor NosTale\n just to learn \nsome python", bg="#263D42", fg="white", width=20)
mainText.grid(column=1, row=0)

label1 = tk.Label(root, text=label_text, bg="#263D42", fg="white", width=20)
label1.grid(column=1, row=2)

# Starte die Haupt-Loop des Fensters
root.mainloop()
