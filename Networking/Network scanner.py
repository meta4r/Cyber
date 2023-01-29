import tkinter as tk
from tkinter import ttk
from scapy.all import ARP, Ether, srp
from threading import Thread
import socket

def scan_network(subnet):
    try:
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{subnet}"), timeout=2)
        for sent, received in ans:
            mac_address = received.sprintf(r"%Ether.src%")
            ip_address = received.sprintf(r"%ARP.psrc%")
            scan_results.insert("", "end", values=(ip_address, mac_address))
        scan_status.set("Scan Completed")
        scan_button.config(state='normal')
        scan_button.config(text="Scan")
    except:
        scan_status.set("Error Occured")

def on_scan_button_click():
    subnet = subnet_var.get()
    scan_status.set("Scanning...")
    scan_button.config(state='disable')
    scan_button.config(text="Scanning...")
    for i in scan_results.get_children():
        scan_results.delete(i)
    Thread(target=scan_network, args=(subnet,)).start()

root = tk.Tk()
root.geometry("720x360")
root.title("Network Scanner")

style = tk.ttk.Style()
style.configure("Treeview", background="black", foreground="white", fieldbackground="white", relief="solid")

scan_button = tk.Button(root, text="Scan", command=on_scan_button_click, bg='#282828', fg='white', font=("Calibri", 16))
scan_button.pack(padx=10, pady=10)

scan_status = tk.StringVar()
scan_status_label = ttk.Label(root, textvariable=scan_status)
scan_status_label.pack()

scan_results = tk.ttk.Treeview(root, columns=("IP Address", "MAC Address"), show="headings", height=10)
scan_results.heading("IP Address", text="IP Address")
scan_results.heading("MAC Address", text="MAC Address")
scan_results.column("IP Address", width=150)
scan_results.column("MAC Address", width=150)
scan_results.pack(padx=10, pady=10)

scan_results.configure(style="Treeview")

subnet_var = tk.StringVar(value="192.168.1.0/24")
subnet_options = ["192.168.1.0/24", "192.168.0.0/24", "10.0.0.0/8"]
subnet_menu = tk.OptionMenu(root, subnet_var, *subnet_options)
subnet_menu.pack()

root.mainloop()
