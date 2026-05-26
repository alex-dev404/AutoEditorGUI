@echo off
title AutoCutStudio Installer
color 0A

echo =========================================
echo        AUTOCUTSTUDIO INSTALLER
echo =========================================
echo.

:: =========================================
:: CHECK ADMIN
:: =========================================

net session >nul 2>&1

if %errorLevel% neq 0 (
    echo Execute este instalador como ADMINISTRADOR.
    pause
    exit
)

:: =========================================
:: PYTHON
:: =========================================

echo.
echo =========================================
echo Instalando Python 3.11...
echo =========================================
echo.

winget install -e --id Python.Python.3.11 --silent

:: =========================================
:: FFMPEG
:: =========================================

echo.
echo =========================================
echo Instalando FFmpeg...
echo =========================================
echo.

winget install -e --id Gyan.FFmpeg --silent

:: =========================================
:: UPDATE PIP
:: =========================================

echo.
echo =========================================
echo Atualizando PIP...
echo =========================================
echo.

python -m pip install --upgrade pip

:: =========================================
:: DEPENDENCIAS PYTHON
:: =========================================

echo.
echo =========================================
echo Instalando dependencias Python...
echo =========================================
echo.

pip install auto-editor
pip install ffmpeg-python
pip install customtkinter
pip install pillow
pip install tkinterdnd2
pip install pyinstaller

:: =========================================
:: TESTE
:: =========================================

echo.
echo =========================================
echo Verificando instalacoes...
echo =========================================
echo.

python --version
ffmpeg -version
auto-editor --version

:: =========================================
:: FINAL
:: =========================================

echo.
echo =========================================
echo      INSTALACAO FINALIZADA!
echo =========================================
echo.
echo Tudo foi instalado com sucesso.
echo.
echo Agora voce pode abrir:
echo.
echo AutoCutStudio.exe
echo.
pause

