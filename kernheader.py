#!/usr/bin/env python3
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import pyfiglet

class FileDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        custom_fig = pyfiglet.Figlet(font='mnemonic')
        banner_text = custom_fig.renderText("kernw0lf")
        banner_label = QLabel(banner_text)
        banner_label.setAlignment(Qt.AlignCenter)
        banner_label.setStyleSheet("color: #007BFF; font-size: 34px;")
        
        self.setWindowTitle('KernHeader')
        self.setWindowIcon(QIcon('icon.ico')) 
        self.setStyleSheet("background-color: #f0f0f0;")

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        window_width, window_height = 950, 850
        self.setGeometry(screen_geometry.center().x() - window_width // 2,
                         screen_geometry.center().y() - window_height // 2,
                         window_width, window_height)

        font = QFont("Arial", 12)
        self.setFont(font)

        self.file_label = QLabel('Enter File Name:')
        self.file_label.setStyleSheet("color: #333;")

        self.file_input = QLineEdit()
        self.file_input.setStyleSheet("background-color: white; border: 1px solid #ccc; color: #000;")

        self.download_button = QPushButton('Download and Display')
        self.download_button.clicked.connect(self.download_and_convert)
        self.download_button.setStyleSheet("background-color: #007BFF; color: white; border: 1px solid #007BFF;")

        self.output_label = QLabel()
        self.output_label.setStyleSheet("color: #333;")

        self.webview = QWebEngineView()
        self.webview.setFixedSize(window_width, window_height-100)
        self.webview.hide()  

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  
        self.progress_bar.setTextVisible(True)  
        self.progress_bar.setVisible(False)  

        hbox = QHBoxLayout()
        hbox.addWidget(self.file_label)
        hbox.addWidget(self.file_input)
        hbox.addWidget(self.download_button)

        layout = QVBoxLayout()
        layout.addWidget(banner_label)  
        layout.addLayout(hbox)  
        layout.addWidget(self.output_label)
        layout.addWidget(self.progress_bar) 
        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.file_input.returnPressed.connect(self.download_button.click)

    def download_and_convert(self):
        file_name = self.file_input.text().strip()
        url = f'https://raw.githubusercontent.com/torvalds/linux/master/include/linux/{file_name}'

        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                error_message = "Error: File name incorrect or not found."
                self.show_warning_message(error_message)
                return

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024 
            self.progress_bar.setMaximum(total_size // block_size)
            self.progress_bar.setVisible(True)  

            with open(f'/tmp/{file_name}', 'wb') as f:
                for data in response.iter_content(block_size):
                    f.write(data)
                    self.progress_bar.setValue(self.progress_bar.value() + 1)

            out_file = f"/tmp/{file_name}.html"
            subprocess.run(['pygmentize', '-o', out_file, '-f', 'html', '-O', 'full,style=dracula', f'/tmp/{file_name}'])
            self.output_label.setText(f"File downloaded and saved to:\n/tmp/{file_name}")

            self.webview.setUrl(QUrl.fromLocalFile(out_file))
            self.webview.show()
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.show_warning_message(error_message)
        finally:
            self.progress_bar.setVisible(False)  

    def show_warning_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setFont(QFont("Arial", 10, QFont.Bold))
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    window = FileDownloader()
    window.show()
    sys.exit(app.exec_())
