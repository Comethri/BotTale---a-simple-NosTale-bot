import tkinter as tk
import win32gui
import win32con
import pymem
import pymem.process
import asyncio
from asyncio import run
from utils import connect_to_packet_logger

bot_running = False
pm = pymem.Pymem("NosTaleClientX.exe")

print("Welcome to BotTale")
print("BotTale is a bot for the game NosTale written in Python")
print("BotTale is currently in development")


async def wait_for_map_change():
    reader = connect_to_packet_logger()
    print("Waiting for map change.")
    while True:
        data = reader.recv(8192)
        if not data:
            continue
        decoded_data = data.decode("utf-8")
        packets = decoded_data.split("\r\n")
        filtered_packets = [packet for packet in packets if packet.startswith("0 c_") and "c_map" in packet or "c_info" in packet or "c_lev" in packet]
        if filtered_packets:
            received_packet = filtered_packets[0]
            print(f"Received packet: {received_packet}")
            if "0 c_info" in received_packet:
                word, number = extract_info_from_packet(received_packet)
                print(f"Extracted word: {word}")
                print(f"Extracted number: {number}")
                return received_packet


async def main():
    port = 13245
    packet_logger = get_nostale_packet_logger_ports(port)
    packet_logger.serve()
    while True:
        print("Waiting for map change.")
        c_map_packet = await packet_logger.wait_for_packet(lambda _packet: _packet[1] == "c_map")
        print("Map have been changed, c_map packet:", c_map_packet)




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

#window that opens when you start the program
root = tk.Tk()
root.title("BotTale")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="#263D42")

button1 = tk.Button(root, text="Start", command=button1_click, bg="white", fg="black", width=10)
button1.grid(column=0, row=0)

button2 = tk.Button(root, text="Stop", command=button2_click, bg="white", fg="black", width=10)
button2.grid(column=0, row=1)

button3 = tk.Button(root, text="Packet", command="handle_map_change", bg="white", fg="black", width=10)
button3.grid(column=0, row=2)

status = "Not started"
label0 = tk.Label(root, text=status)
label0.grid(column=0, row=3, sticky="W")

#player label
player = tk.Label(root, text="Player")
player.grid(column=2, row=0, sticky="W", padx=5)

label2 = tk.Label(root)
label2.grid(column=2, row=1, sticky="W", padx=5)

label3 = tk.Label(root)
label3.grid(column=2, row=2, sticky="W", padx=5)

label6 = tk.Label(root)
label6.grid(column=2, row=3, sticky="W", padx=5)

label7 = tk.Label(root)
label7.grid(column=2, row=4, sticky="W", padx=5)

input0 = tk.Entry(root)
input0.grid(column=3, row=1, sticky="W", padx=5)

#target label
target = tk.Label(root, text="Target")
target.grid(column=4, row=0, sticky="W", padx=10)

label4 = tk.Label(root)
label4.grid(column=4, row=1, sticky="W", padx=10)

label5 = tk.Label(root)
label5.grid(column=4, row=2, sticky="W", padx=10)

update_values()
# asyncio.run(main())
root.mainloop()
