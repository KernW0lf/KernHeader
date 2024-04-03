import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
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

        hbox = QHBoxLayout()
        hbox.addWidget(self.file_label)
        hbox.addWidget(self.file_input)
        hbox.addWidget(self.download_button)

        layout = QVBoxLayout()
        layout.addWidget(banner_label)  
        layout.addLayout(hbox)  
        layout.addWidget(self.output_label)
        layout.addWidget(self.webview)

        self.setLayout(layout)

    def download_and_convert(self):
        file_name = self.file_input.text().strip()
        url = f'https://raw.githubusercontent.com/torvalds/linux/master/include/linux/{file_name}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(f'/tmp/{file_name}', 'wb') as f:
                    f.write(response.content)

                out_file = f"/tmp/{file_name}.html"
                subprocess.run(['pygmentize', '-o', out_file, '-f', 'html', '-O', 'full,style=dracula', f'/tmp/{file_name}'])
                self.output_label.setText(f"File downloaded and saved to:\n/tmp/{file_name}")


                self.webview.setUrl(QUrl.fromLocalFile(out_file))
                self.webview.show()  
            else:
                self.output_label.setStyleSheet("color: #333; font-size: 20px;") 
                self.output_label.setText("File not found. Please enter a valid file name.")
        except Exception as e:
            self.output_label.setText(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    window = FileDownloader()
    window.show()
    sys.exit(app.exec_())
