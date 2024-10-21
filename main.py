import sys
import socket
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QMenuBar, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QAction

class IpGrabber(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Grabber - SYSINT Proj 3")
        self.setGeometry(100, 100, 400, 200)

        # Layout and Widgets
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout);

        self.header_label = QLabel("<h1>IPGrabber</h1>")

        self.subtitle_label = QLabel("<p>Your public IP address are listed below:</p>\n\n")
        self.ipv4_label = QLabel("<b>IPv4: Fetching...</b>")
        self.ipv6_label = QLabel("<b>IPv6: Fetching...</b>")

        self.geolocation_label = QLabel("<h2>Geolocation:</h2>")
        self.country_label = QLabel("<p>Country: Fetching...</p>")
        self.region_label = QLabel("<p>Region: Fetching...</p>")
        self.city_label = QLabel("<p>City: Fetching...</p>")

        self.fetch_button = QPushButton("Fetch IP Addresses")
        self.fetch_button.clicked.connect(self.fetch_ip_addresses)

        # Add widgets to layout
        self.setCentralWidget(central_widget)
        
        layout.addWidget(self.header_label)
        layout.addItem(QSpacerItem(10, 10))
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.ipv4_label)
        layout.addWidget(self.ipv6_label)
        layout.addItem(QSpacerItem(10, 10))
        layout.addWidget(self.geolocation_label)
        layout.addWidget(self.country_label)
        layout.addWidget(self.region_label)
        layout.addWidget(self.city_label)

        layout.addItem(QSpacerItem(10, 20))
        layout.addWidget(self.fetch_button)

        # Add menu bar
        self._createMenuBar()

        # Initial fetch
        self.fetch_ip_addresses()
        self.fetch_geolocation()

    def _createMenuBar(self):
        menuBar = QMenuBar(self)

        helpMenu = menuBar.addMenu("&File")

        # About Action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._onAboutActionClick)
        helpMenu.addAction(about_action)

        # Exit App Action
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self._onExitActionClick)
        helpMenu.addAction(exit_action)

        self.setMenuBar(menuBar)

    def _onAboutActionClick(self, s):        
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About this program")
        about_dialog.setText(
            "<h1>IPGrabber</h1>\n\n"
            "<p>SysInt Project 3</p>\n\n"
            "<p>Version 0.0.1<br/>\n\n\n"
            "<p>Authors:</p>\n\n"
            "<p>Jasper Arangali</p>\n"
            "<p>Mika Cruz</p>\n"
            "<p>Luis Granada</p>\n"
            "<p>Angela Marie Ronquillo</p>\n"
            "<p>Vincent Paul Tampos</p>\n"
        )
        about_dialog.setIcon(QMessageBox.Icon.Information)
        about_dialog.setMinimumSize(400, 300)

        about_dialog.exec()

    def _onExitActionClick(self, s):
        sys.exit(app.exec())

    def fetch_geolocation(self):
        try:
            res = self.fetch_api("https://ipapi.co/json/")
            self.country_label.setText(f"<p>Country: {res['country_name']}</p>")
            self.region_label.setText(f"<p>Region: {res['region']}</p>")
            self.city_label.setText(f"<p>City: {res['city']}</p>")
        except requests.RequestException as e:
            self.show_error(f"Error fetching country: {str(e)}")

    @staticmethod
    def has_ipv6():
        try:
            # Create a socket for IPv6 and attempt a connection.
            test_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            test_socket.settimeout(5)  # 5-second timeout
            test_socket.connect(("ipv6.google.com", 80))
            test_socket.close()
            return True
        except (OSError, socket.timeout) as e:
            # Catch multiple exceptions properly
            print(f"IPv6 check failed: {e}")
            return False

    def fetch_ip_addresses(self):
        # IPv4 & Geolocation
        try:
            res = self.fetch_api("https://api.ipify.org?format=json")
            self.ipv4_label.setText(f"<b>IPv4: {res['ip']}</b>")
        except requests.RequestException as e:
            self.show_error(f"Error fetching IPv4: {str(e)}")

        if (self.has_ipv6()):
            try:
                res = self.fetch_api("https://api64.ipify.org?format=json")
                self.ipv6_label.setText(f"<b>IPv6: {res['ip']}</b>")
            except requests.RequestException as e:
                self.show_error(f"Error fetching IPv6: {str(e)}")
        else:
            self.ipv6_label.setText("<b>IPv6: Not available</b>")

    @staticmethod
    def fetch_api(url):
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        return response.json()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = IpGrabber()
    window.show()
    
    sys.exit(app.exec())
