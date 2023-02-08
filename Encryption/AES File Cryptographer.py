import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedTk
from Crypto.Cipher import AES
import os

def get_file_path():
    file_path = filedialog.askopenfilename()
    file_path_label.config(text=file_path)
    return file_path

def encrypt_file():
    file_path = get_file_path()
    key = key_entry.get().encode()
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    data = open(file_path, 'rb').read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path + '.encrypted', 'wb') as f:
        [ f.write(x) for x in (nonce, ciphertext, tag) ]

def decrypt_file():
    file_path = get_file_path()
    key = key_entry.get().encode()
    with open(file_path, 'rb') as f:
        nonce, ciphertext, tag = [ f.read(x) for x in (16, os.path.getsize(file_path)-32, 16) ]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file_path + '.decrypted', 'wb') as f:
        f.write(data)

root = ThemedTk(theme="black")

# file path label
file_path_label = tk.Label(root)
file_path_label.pack()

# key entry field
key_label = tk.Label(root, text="Enter key:")
key_label.pack()
key_entry = tk.Entry(root, show="*", width=20)
key_entry.pack()

# file picker button
file_picker_button = tk.Button(root, text="Pick file", command=get_file_path)
file_picker_button.pack()

# encrypt button
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file)
encrypt_button.pack()

# decrypt button
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file)
decrypt_button.pack()

root.mainloop()
