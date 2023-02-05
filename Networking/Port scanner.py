import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Tool to scan ports on a network
def scan_ports(host, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def start_scan():
    global host
    host = host_entry.get()
    global open_ports
    open_ports = scan_ports(host, 1, 65535)
    for port in open_ports:
        port_list.insert(tk.END, f"Port {port} is open")
    for port in range(1,65535):
        if port not in open_ports:
            port_list.insert(tk.END, f"Port {port} is closed")
    scan_button.config(state="disable")
    stop_button.config(state="normal")

def stop_scan():
    scan_button.config(state="normal")
    stop_button.config(state="disable")
    port_list.delete(0, tk.END)

root = tk.Tk()
root.title("Port Scanner")

host_label = ttk.Label(root, text="Enter host:")
host_label.grid(row=0, column=0, padx=5, pady=5)

host_entry = ttk.Entry(root)
host_entry.grid(row=0, column=1, padx=5, pady=5)

scan_button = ttk.Button(root, text="Scan", command=start_scan)
scan_button.grid(row=1, column=0, padx=5, pady=5)

stop_button = ttk.Button(root, text="Stop", command=stop_scan, state="disable")
stop_button.grid(row=1, column=1, padx=5, pady=5)

port_list = tk.Listbox(root, width=50)
port_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
