#!/usr/bin/env python3
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QMessageBox, QCheckBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QUrl
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

        screen_geometry = QApplication.primaryScreen().geometry()
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

        self.search_label = QLabel('Search Text:')
        self.search_label.setStyleSheet("color: #333;")

        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: white; border: 1px solid #ccc; color: #000;")
        self.search_input.returnPressed.connect(self.highlight_text)  

        self.match_count_label = QLabel()
        self.match_count_label.setStyleSheet("color: #333;")

        self.download_button = QPushButton('Download and Display')
        self.download_button.clicked.connect(self.download_and_convert)
        self.download_button.setStyleSheet("background-color: #007BFF; color: white; border: 1px solid #007BFF;")

        self.output_label = QLabel()
        self.output_label.setStyleSheet("color: #333;")

        self.webview = QWebEngineView()
        self.webview.setFixedSize(window_width, window_height - 100)
        self.webview.hide()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  
        self.progress_bar.setTextVisible(True)  
        self.progress_bar.setVisible(False) 

        self.toggle_highlight_button = QCheckBox('Highlight')
        self.toggle_highlight_button.setStyleSheet("color: #333;")
        self.toggle_highlight_button.stateChanged.connect(self.toggle_highlight)

        hbox_file = QHBoxLayout()
        hbox_file.addWidget(self.file_label)
        hbox_file.addWidget(self.file_input)
        hbox_file.addWidget(self.download_button)

        hbox_search = QHBoxLayout()
        hbox_search.addWidget(self.search_label)
        hbox_search.addWidget(self.search_input)
        hbox_search.addWidget(self.match_count_label)  
        hbox_search.addWidget(self.toggle_highlight_button)

        layout = QVBoxLayout()
        layout.addWidget(banner_label)
        layout.addLayout(hbox_file)
        layout.addLayout(hbox_search)  
        layout.addWidget(self.output_label)
        layout.addWidget(self.progress_bar)  
        layout.addWidget(self.webview)

        self.setLayout(layout)
        self.file_input.returnPressed.connect(self.download_button.click)


    def highlight_text(self):
        text_to_find = self.search_input.text().strip()
        if text_to_find:
            script_clear = "document.body.innerHTML = document.body.innerHTML.replace(/<span style=\"background-color: lightyellow;\">(.*?)<\/span>/g, '$1');"
            script_highlight = f"var matches = document.body.innerHTML.match(new RegExp('{text_to_find}', 'gi'));"
            script_highlight += f"document.body.innerHTML = document.body.innerHTML.replace(new RegExp('{text_to_find}', 'gi'), '<span style=\"background-color: lightyellow;\">{text_to_find}</span>');"
            script_highlight += "matches ? matches.length : 0;"  
            final_script = script_clear + script_highlight

            def callback(result):
                self.match_count_label.setText(f"Matches found: {result}")

            self.webview.page().runJavaScript(final_script, callback)
        else:
            self.match_count_label.setText("") 


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

    def toggle_highlight(self, state):
        if state == Qt.Checked:
            self.highlight_text()
        else:
            self.clear_highlight()

    def clear_highlight(self):
        script_clear = "document.body.innerHTML = document.body.innerHTML.replace(/<span style=\"background-color: lightyellow;\">(.*?)<\/span>/g, '$1');"
        self.webview.page().runJavaScript(script_clear)

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
