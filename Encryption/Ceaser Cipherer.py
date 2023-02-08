import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

#PyQt GUI
class CaesarCipherUI(QWidget):
    def __init__(self):
        super().__init__()

        self.input_label = QLabel("Enter text or cipher:")
        self.input_box = QLineEdit()
        self.shift_label = QLabel("Choose shift value (1-25):")
        self.shift_box = QLineEdit()
        self.encrypt_button = QPushButton("Encrypt")
        self.decrypt_button = QPushButton("Decrypt")

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)

        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.shift_label)
        layout.addWidget(self.shift_box)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        self.setLayout(layout)

        self.setWindowTitle("Caesar Cipher")
        self.show()

#Encryption

    def encrypt(self):
        plaintext = self.input_box.text()
        shift = int(self.shift_box.text())
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                shift_char = chr((ord(char) + shift - 65) % 26 + 65)
                ciphertext += shift_char
            else:
                ciphertext += char
        self.input_box.setText(ciphertext)

    def decrypt(self):
        ciphertext = self.input_box.text()
        shift = int(self.shift_box.text())
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                shift_char = chr((ord(char) - shift - 65) % 26 + 65)
                plaintext += shift_char
            else:
                plaintext += char
        self.input_box.setText(plaintext)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CaesarCipherUI()
    sys.exit(app.exec_())