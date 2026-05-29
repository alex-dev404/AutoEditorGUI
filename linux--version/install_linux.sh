#!/bin/bash

echo "==================================="
echo "   AutoCutStudio Linux Installer"
echo "==================================="

echo ""
echo "Instalando FFmpeg..."
sudo apt update
sudo apt install ffmpeg -y

echo ""
echo "Instalando Python..."
sudo apt install python3 python3-pip -y

echo ""
echo "Instalando dependências..."

pip3 install auto-editor
pip3 install customtkinter
pip3 install pillow
pip3 install tkinterdnd2
pip3 install ffmpeg-python

echo ""
echo "==================================="
echo "Instalação concluída!"
echo "==================================="