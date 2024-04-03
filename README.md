# KernHeader
KernHeader is a simple Python application built with PyQt5 for downloading Linux kernel header files from the Linux repository and displaying them in a syntax-highlighted HTML format using Pygments.

## Features
* File Download: Download Linux kernel header files from the official Linux repository.
* Syntax Highlighting: Display downloaded files in an HTML format with syntax highlighting.
* User-friendly Interface: Simple GUI built with PyQt5 for easy file input and display.

## Installation
To use KernHeader, you'll need Python 3.x installed on your system.

### 1. Clone this repository:
```bash
git clone https://github.com/KernW0lf/KernHeader.git
```

### 2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

If you face any error related to PyQt5-QTWebEngine, use the following commands:

```bash
pip uninstall PyQt5 PyQt5-tools PyQt5-sip
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine
```

## Usage

### 1. Run the application:

```bash
python kernheader.py
```

### 2. Enter the name of the Linux kernel header file you want to download in the input field.

### 3. Click on the "Download and Display" button.

### 4. If the file is found, it will be downloaded, converted to HTML with syntax highlighting, and displayed in the application.

### 5. If the file is not found, an error message will be displayed.

## Contributing

Contributions are welcome! If you'd like to contribute to KernHeader, please fork the repository and create a pull request with your changes.

## Credits

    PyQt5
    Pygments
    pyfiglet
    Requests

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/KernW0lf/KernHeader/blob/main/LICENSE) file for details.
