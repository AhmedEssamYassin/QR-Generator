# QR Code Generator Pro

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.x-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

A professional, feature-rich QR Code Generator desktop application built with Python and ttkbootstrap. Create fully customizable QR codes for various purposes with a modern, user-friendly interface.

## Features

- **Multiple Data Types**:
  - **Text**: Plain text messages
  - **URL**: Website links (auto-adds https://)
  - **Email**: Pre-filled emails with subject and body
  - **Phone**: Click-to-call phone numbers
  - **WiFi**: WiFi network credentials (WPA/WEP/No Pass)
  - **vCard**: Digital contact cards

- **Advanced Customization**:
  - **Styles**: Standard Square, Rounded, Circle, and Gapped Square module drawers
  - **Colors**: Custom Foreground and Background colors
  - **Size Control**: Adjustable box size and border width
  - **Error Correction**: 4 levels (Low, Medium, Quartile, High)

- **Productivity Tools**:
  - **Dark/Light Mode**: Seamless theme switching
  - **History**: Automatically saves generation history for quick reuse
  - **Clipboard**: Copy generated QR codes directly to clipboard
  - **Export**: Save as PNG, JPG, BMP, or GIF

## Architecture Overview

### System Design (UML Diagram)
![UML Diagram](./docs/system%20design%20UML.svg)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AhmedEssamYassin/QR-Generator.git
   cd QR-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application from source:

```bash
python main.py
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+G` | Generate QR Code |
| `Ctrl+S` | Save Image |
| `Ctrl+C` | Copy to Clipboard |
| `F1` | Show Help |

## Building the Executable

This project includes a custom build script to compile the application into a standalone `.exe` using PyInstaller.

1. **Run the build script:**
   ```bash
   python build.py
   ```

2. **Select your build preference** from the menu:
   - **Option 1**: One File (Single `.exe`, portable)
   - **Option 2**: One Directory (Faster startup, folder based)

The output will be located in the `dist/` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Author**: Ahmed Yassin  
**Copyright**: © 2026 AhmedEssamYassin