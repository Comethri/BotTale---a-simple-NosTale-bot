import tkinter as tk
import win32gui
import win32con
import pymem
import pymem.process

bot_running = False
pm = pymem.Pymem("NosTaleClientX.exe")

print("Welcome to BotTale")
print("BotTale is a bot for the game NosTale written in Python")
print("BotTale is currently in development")


# für die values aus NosTale
def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i !=offsets[-1]:
            addr = pm.read_int(addr + i)
        else:
            addr += i
    return addr

gameModule = pymem.process.module_from_name(pm.process_handle, "NosTaleClientX.exe").lpBaseOfDll
HP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x4C])
MP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0x4C])
maxHP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC4, 0x48])
maxMP_address = GetPtrAddr(gameModule + 0x004B2EEC, [0xC8, 0x48])
targetHP_address = GetPtrAddr(gameModule + 0x004B2EF0, [0xFC, 0x4C])
targetMP_address = GetPtrAddr(gameModule + 0x004B2EF0, [0x100, 0x4C])
targetmaxHP_address = GetPtrAddr(gameModule + 0x004B2EF0, [0xFC, 0x48])
targetmaxMP_address = GetPtrAddr(gameModule + 0x004B2EF0, [0x100, 0x48])
xP_address = GetPtrAddr(gameModule + 0x004B324C, [0x158])
lvl_address = GetPtrAddr(gameModule + 0x004B313C, [0x80])

def calculate_percentage(value, max_value):
    return f"{value}/{max_value} ({int(value / max_value * 100)}%)"

def update_values():
    global valueHP, valuemaxHP, valueMP, valuemaxMP, valueTargetmaxHP, valueTargetHP, valueTargetmaxMP, valueTargetMP, valueXP, valueLvl
    valueHP = pm.read_int(HP_address)
    valuemaxHP = pm.read_int(maxHP_address)
    valueMP = pm.read_int(MP_address)
    valuemaxMP = pm.read_int(maxMP_address)
    valueTargetHP = pm.read_int(targetHP_address)
    valueTargetMP = pm.read_int(targetMP_address)
    valueTargetmaxHP = pm.read_int(targetmaxHP_address)
    valueTargetmaxMP = pm.read_int(targetmaxMP_address)
    valueXP = pm.read_int(xP_address)
    valueLvl = pm.read_int(lvl_address)

    label_text2 = f"HP:{calculate_percentage(valueHP, valuemaxHP)}"
    label_text3 = f"MP:{calculate_percentage(valueMP, valuemaxMP)}"
    label_text4 = f"HP:{calculate_percentage(valueTargetHP, valueTargetmaxHP)}"
    label_text5 = f"MP:{calculate_percentage(valueTargetMP, valueTargetmaxMP)}"
    label_text6 = f"XP:{valueXP}%"
    label_text7 = f"LV:{valueLvl}"

    label2.config(text=label_text2)
    label3.config(text=label_text3)
    label4.config(text=label_text4)
    label5.config(text=label_text5)
    label6.config(text=label_text6)
    label7.config(text=label_text7)

    root.after(500, update_values)


# spacebar bot via keypress
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
        hwnd = win32gui.FindWindow(None, "NosTale")
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

def cella_calc():
    calc = tk.Tk()
    calc.title("Cella Calc")
    calc.resizable(False, False)
    calc["bg"] = "#454545"

    gillion = tk.Label(calc, text="Gillion", background="#454545", fg="white", padx=5, pady=5)
    gillion.grid(column=0, row=0, sticky="W")

    gillion_entry = tk.Entry(calc, width=10)
    gillion_entry.grid(column=1, row=0)
    gillion_entry.insert(0, "1000")

    gillion_entry_price = tk.Entry(calc, width=10)
    gillion_entry_price.grid(column=2, row=0)
    gillion_entry_price.insert(0, "0")

    gillion_full_price = tk.Label(calc, text="?", background="#454545", fg="white")
    gillion_full_price.grid(column=3, row=0, sticky="W")

    veredler = tk.Label(calc, text="Veredler", background="#454545", fg="white", padx=5, pady=5)
    veredler.grid(column=0, row=1, sticky="W")

    veredler_entry = tk.Entry(calc, width=10)
    veredler_entry.grid(column=1, row=1)
    veredler_entry.insert(0, "1000")

    veredler_entry_price = tk.Entry(calc, width=10)
    veredler_entry_price.grid(column=2, row=1)
    veredler_entry_price.insert(0, "500")

    veredler_full_price = tk.Label(calc, text="?", background="#454545", fg="white")
    veredler_full_price.grid(column=3, row=1, sticky="W")

    cella = tk.Label(calc, text="Cella", background="#454545", fg="white", padx=5, pady=5)
    cella.grid(column=0, row=2, sticky="W")

    cella_entry = tk.Entry(calc, width=10)
    cella_entry.grid(column=1, row=2)
    cella_entry.insert(0, "7500")

    cella_entry_price = tk.Entry(calc, width=10)
    cella_entry_price.grid(column=2, row=2)
    cella_entry_price.insert(0, "0")

    cella_full_price = tk.Label(calc, text="?", background="#454545", fg="white")
    cella_full_price.grid(column=3, row=2, sticky="W")

    calc_win_lose = tk.Label(calc, text="Win/Lose", background="#454545", fg="white")
    calc_win_lose.grid(column=3, row=3, sticky="W")

    def calculate(*args):
        try:
            value1 = int(gillion_entry.get())
            value2 = int(gillion_entry_price.get())
            result = value1 * value2
            gillion_full_price.config(text=result)

            value3 = int(veredler_entry.get())
            value4 = int(veredler_entry_price.get())
            result2 = value3 * value4
            veredler_full_price.config(text=result2)

            value5 = int(cella_entry.get())
            value6 = int(cella_entry_price.get())
            result3 = value5 * value6
            cella_full_price.config(text=result3)
            
            result4 = result3 - result2 - result
            calc_win_lose.config(text=result4)
            if result4 < 0:
                calc_win_lose.config(fg="red")
            else:
                calc_win_lose.config(fg="green")
        except ValueError:
            pass

    gillion_entry.bind("<KeyRelease>", calculate)
    gillion_entry_price.bind("<KeyRelease>", calculate)
    veredler_entry.bind("<KeyRelease>", calculate)
    veredler_entry_price.bind("<KeyRelease>", calculate)
    cella_entry.bind("<KeyRelease>", calculate)
    cella_entry_price.bind("<KeyRelease>", calculate)








    calc.mainloop()



#window that opens when you start the program
root = tk.Tk()
root.title("BotTale")
root.resizable(False, False)
root["bg"] = "#454545"


button1 = tk.Button(root, text="Start", command=button1_click, bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click, bg="white", fg="black", width=10)
button2.grid(column=0, row=1)

button3 = tk.Button(root, text="Cella Calc", command=cella_calc, bg="white", fg="black", width=10)
button3.grid(column=0, row=2)

status = "Not started"
label0 = tk.Label(root, text=status, background="#454545", fg="white")
label0.grid(column=0, row=3, sticky="W")

#player label
player = tk.Label(root, text="Player", background="#454545", fg="white")
player.grid(column=2, row=0, sticky="W", padx=5)

label2 = tk.Label(root, background="#454545", fg="white")
label2.grid(column=2, row=1, sticky="W", padx=5)

label3 = tk.Label(root, background="#454545", fg="white")
label3.grid(column=2, row=2, sticky="W", padx=5)

label6 = tk.Label(root, background="#454545", fg="white")
label6.grid(column=2, row=3, sticky="W", padx=5)

label7 = tk.Label(root, background="#454545", fg="white")
label7.grid(column=2, row=4, sticky="W", padx=5)

#target label
target = tk.Label(root, text="Target", background="#454545", fg="white")
target.grid(column=4, row=0, sticky="W", padx=10)

label4 = tk.Label(root, background="#454545", fg="white")
label4.grid(column=4, row=1, sticky="W", padx=10)

label5 = tk.Label(root, background="#454545", fg="white")
label5.grid(column=4, row=2, sticky="W", padx=10)

update_values()
root.mainloop()
