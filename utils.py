from typing import List
import socket
from psutil import process_iter, AccessDenied, Process

# Funktionen, um Prozesse und zugehörige Ports zu erhalten
def get_processes(substring: str) -> List[Process]:
    processes = []
    for process in process_iter():
        try:
            if substring in process.name():
                processes.append(process)
        except AccessDenied as err:
            pass
    return processes

def get_nostale_packet_logger_ports() -> List[int]:
    processes = get_processes("NostaleClientX.exe")
    ports = []
    for process in processes:
        for connection in process.connections():
            if connection.laddr and connection.laddr.ip == "127.0.0.1":
                port = connection.laddr.port
                ports.append(port)
                print(f"Packet logger port: {ports}")
            #when no connection, make alterbox
            if not connection.laddr:
                print("No connection")
    return ports

def connect_to_packet_logger():
    PACKET_LOGGER_IP = "127.0.0.1"
    PACKET_LOGGER_PORT = get_nostale_packet_logger_ports()[0]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((PACKET_LOGGER_IP, PACKET_LOGGER_PORT))
        print("Connected to packet logger")
    except ConnectionRefusedError:
        print("Connection to packet logger refused")
        return None
    return sock

def receive_packet(sock, filters=None):
    data = sock.recv(8192)
    if not data:
        return None
    decoded_data = data.decode("utf-8")
    packets = decoded_data.split("\r\n")
    if filters:
        packets = [packet for packet in packets if any(keyword in packet for keyword in filters)]
    return packets
