import sys
import wifi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

class WiFiScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('WiFi Scanner')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.wifi_scanner = wifi.Cell.all('wlan0')
        for network in self.wifi_scanner:
            security = self.analyze_security(network)
            btn = QPushButton(f"{network.ssid} - Channel: {network.channel} - Frequency: {network.frequency} MHz - Signal Strength: {network.signal} dBm - Encryption: {network.encryption_type} - Security: {security}")
            btn.clicked.connect(lambda state, x=network: self.show_details(x))
            layout.addWidget(btn)

    def analyze_security(self, network):
        if network.encrypted:
            if network.encryption_type in ["wpa2", "wpa"]:
                return "secure"
            else:
                return "less secure"
        else:
            return "insecure"

    def show_details(self, network):
        details = f"SSID: {network.ssid}\n"
        details += f"BSSID: {network.address}\n"
        details += f"Encryption Type: {network.encryption_type}\n"
        details += f"Channel: {network.channel}\n"
        details += f"Frequency: {network.frequency} MHz\n"
        details += f"Signal Strength: {network.signal} dBm\n"
        details += f"Max Data Rate: {network.maxrate} Mbps\n"
        details += f"Capabilities: {network.capabilities}\n"
        label = QLabel(details)
        label.setAlignment(Qt.AlignCenter)
        label.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner = WiFiScanner()
    scanner.show()
    sys.exit(app.exec_())