# AutoEditorGUI

Modern GUI for Auto-Editor on Windows and Linux.

A modern desktop interface for the amazing Auto-Editor project, focused on speed, automation and video editor workflow.

---

# Features

- Modern Windows 11 style interface
- Automatic silence cutting
- Margin slider control
- Multi-video batch processing
- Export directly to:
  - DaVinci Resolve
  - Adobe Premiere
  - Final Cut Pro
  - Shotcut
  - Kdenlive
- Automatic dependency installer
- Real-time processing status
- Simple EXE generation
- Lightweight and fast

---

# Preview

## Main Features

- Select video folder
- Automatic video detection
- Real-time progress updates
- Margin editor
- Export presets
- Processing logs

---

# Built With

- Python
- CustomTkinter
- Auto-Editor
- FFmpeg
- PyInstaller

---

# Installation

## Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/AutoCutStudio.git
cd AutoCutStudio
```

---

# Install dependencies

```bash
pip install customtkinter
pip install auto-editor
pip install ffmpeg-python
```

---

# Run application

```bash
python app.py
```

---

# Generate EXE

```bash
pyinstaller --onefile --windowed app.py
```

---

# Windows Build

Recommended:

```bash
pyinstaller --onefile --windowed --clean app.py
```

With icon:

```bash
pyinstaller --onefile --windowed --icon=icon.ico app.py
```

---

# Linux Version

Linux support is planned.

Future Linux support includes:

- Ubuntu
- Fedora
- Arch Linux
- Linux Mint

Example Linux setup:

```bash
sudo apt install ffmpeg
pip install auto-editor
pip install customtkinter
```

Run:

```bash
python3 app.py
```

---

# Supported Export Formats

| Editor | Supported |
|--------|------------|
| DaVinci Resolve | ✅ |
| Adobe Premiere | ✅ |
| Final Cut Pro | ✅ |
| Shotcut | ✅ |
| Kdenlive | ✅ |

---

# How It Works

The app uses Auto-Editor to detect:

- silence
- loud sections
- pauses
- dead moments

Then automatically creates editable timelines for professional editors.

---

# Project Structure

```text
AutoCutStudio/
│
├── app.py
├── README.md
├── requirements.txt
├── icon.ico
├── assets/
└── dist/
```

---

# Future Improvements

## Planned Features

### UI Improvements
- Timeline preview
- Drag and drop support
- Real video thumbnails
- Dark/Light mode
- Custom themes

### Editing Features
- MP4 direct export
- Auto subtitle generation
- AI scene detection
- Audio normalization
- Multi-track support

### Performance
- GPU acceleration
- Multi-thread processing
- Background rendering
- Queue system

### Advanced Features
- Real video preview
- Timeline zoom
- XML timeline preview
- Preset manager
- Custom export profiles

### Linux & MacOS
- Native Linux package
- AppImage support
- MacOS support

---

# Requirements

- Python 3.11+
- FFmpeg
- Auto-Editor

---

# Screenshots

Coming soon.

---

# Credits

Huge thanks to:

## Auto-Editor
https://github.com/WyattBlue/auto-editor

---

# License

MIT License

---

# Contributing

Pull requests are welcome.

For major changes, please open an issue first.

---

# Roadmap

## Version 1.0
- Basic GUI
- Batch processing
- Export presets

## Version 1.5
- Timeline preview
- Drag and drop
- Progress bar

## Version 2.0
- Full editor-style interface
- Video preview
- GPU acceleration

---

# Author

Developed by alex-dev404 / Alex dos Santos

---

# Star the project

If this project helps you, leave a star on GitHub.
