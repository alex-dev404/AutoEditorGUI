#!/bin/bash

echo "==================================="
echo "   AutoCutStudio Linux Installer"
echo "==================================="

echo ""
echo "Atualizando pacotes..."
sudo apt update

echo ""
echo "Instalando FFmpeg..."
sudo apt install ffmpeg -y

echo ""
echo "Instalando Python e ferramentas..."
sudo apt install python3 python3-pip python3-venv pipx -y

echo ""
echo "Instalando dependências..."

# 1. Tentativa com pipx (isolado e seguro)
if command -v pipx &> /dev/null; then
    echo "Usando pipx..."
    pipx install auto-editor
    pipx install customtkinter
    pipx install pillow
    pipx install tkinterdnd2
    pipx install ffmpeg-python
fi

# 2. Tentativa com venv (isolado por projeto)
echo ""
echo "Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install auto-editor customtkinter pillow tkinterdnd2 ffmpeg-python
deactivate

# 3. Tentativa com pip normal (forçando se necessário)
echo ""
echo "Instalando com pip3 (system)..."
pip3 install auto-editor customtkinter pillow tkinterdnd2 ffmpeg-python --break-system-packages || true

echo ""
echo "==================================="
echo "Instalação concluída!"
echo "==================================="
echo "Você pode rodar o programa com:"
echo "  source venv/bin/activate && python3 main.py"
echo "Ou usar o executável gerado pelo PyInstaller."
