# AutoCutStudio 🎬

Interface profissional para o **Auto-Editor** com:

* Drag & Drop
* Export para Premiere / Resolve / Kdenlive
* Motion Detection
* Audio Threshold
* Thumbnails automáticas
* Progress Bar
* Logs em tempo real
* Interface moderna estilo editor de vídeo

---

# ✨ Preview

```text
✔ Drag and Drop de vídeos
✔ Processamento automático
✔ Export profissional
✔ Interface moderna
✔ Instalação automática de dependências
✔ Compatível com Windows
```

---

# 🚀 Tecnologias

* Python 3.11
* CustomTkinter
* Auto-Editor
* FFmpeg
* Pillow
* TkinterDnD2

---

# 📦 Instalação

# 1️⃣ Baixe o projeto

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/AutoCutStudio-PRO.git
```

ou baixe o ZIP.

---

# 2️⃣ Execute o instalador

Clique duas vezes em:

```text
install_auto_editor.bat
```

Esse script instala automaticamente:

* Python 3.11
* FFmpeg
* Auto-Editor
* Dependências do app

---

# ⚠ IMPORTANTE

Execute o `.bat` como:

```text
Administrador
```

---

# 🧠 O que o instalador faz

O script instala:

```text
✔ Python 3.11
✔ FFmpeg
✔ auto-editor
✔ customtkinter
✔ pillow
✔ tkinterdnd2
✔ ffmpeg-python
✔ pyinstaller
```

---

# ▶ Como abrir o programa

Depois da instalação:

## Modo Python

```bash
python app.py
```

---

## Modo EXE

```text
AutoCutStudio PRO.exe
```

---

# 🛠 Como gerar o EXE

```bash
pyinstaller ^
--onefile ^
--windowed ^
--clean ^
--noconfirm ^
--name "AutoCutStudio PRO" ^
--icon=icone.ico ^
app.py
```

---

# 🎞 Exportações Suportadas

| Editor          | Export      |
| --------------- | ----------- |
| DaVinci Resolve | `.drt`      |
| Premiere Pro    | `.xml`      |
| Final Cut       | `.fcpxml`   |
| Shotcut         | `.mlt`      |
| Kdenlive        | `.kdenlive` |

---

# 🎯 Funções da Interface

# 📂 Selecionar Pasta

Carrega automaticamente todos os vídeos da pasta.

Formatos suportados:

```text
.mp4
.mov
.avi
.mkv
.webm
```

---

# 🖱 Drag & Drop

Você pode arrastar:

* vídeos
* múltiplos vídeos

diretamente para o app.

---

# 🎬 Margin / Corte

O principal sistema de corte automático.

## Padrão:

```text
0.20 sec
```

Esse valor adiciona pequenos espaços antes e depois dos cortes para deixar a edição mais natural.

Exemplo:

```text
0.20 sec
```

Adiciona:

* 0.20s antes
* 0.20s depois

dos cortes detectados.

---

# ⬅ Margin Before

Desativado por padrão.

Controla quanto tempo será preservado:

* ANTES do corte

Exemplo:

```text
0.50 sec
```

Mantém:

```text
0.5 segundos antes
```

do trecho detectado.

---

# ➡ Margin After

Desativado por padrão.

Controla quanto tempo será preservado:

* DEPOIS do corte

Exemplo:

```text
1.00 sec
```

Mantém:

```text
1 segundo depois
```

do trecho detectado.

---

# 🧩 Padding

Desativado por padrão.

Usado para adicionar espaço extra de segurança em cortes agressivos.

Ajuda em:

* vídeos rápidos
* gameplay
* vídeos com respiração curta
* cortes muito secos

---

# 🔊 Audio Threshold

Sistema de detecção de silêncio.

Medido em:

```text
dB
```

Quanto MAIOR o valor:

* mais agressivo o corte

---

## Exemplos

### `-5 dB`

Corta apenas silêncios muito fortes.

### `-20 dB`

Corta pausas médias.

### `-35 dB`

Corta praticamente tudo que estiver baixo.

---

# 🎥 Motion Detection

Sistema experimental de detecção de movimento.

Permite cortar:

* trechos sem movimento
* telas paradas
* pausas visuais

Muito útil para:

* gameplay
* webcam
* podcast
* react

---

# 🖼 Thumbnails Automáticas

O app gera previews automáticas dos vídeos usando:

* FFmpeg
* Pillow

---

# 📊 Progress Bar

Mostra:

* instalação de dependências
* progresso do processamento
* conclusão dos vídeos

---

# 📝 Logs em Tempo Real

O painel de logs mostra:

* comandos executados
* erros
* status do Auto-Editor
* progresso

---

# 📁 Salvamento dos Arquivos

Os arquivos exportados são salvos:

```text
no mesmo local do vídeo original
```

---

# 💡 Exemplo

```text
video.mp4
↓
video.xml
```

ou:

```text
video.kdenlive
video.drt
video.fcpxml
```

---

# 🧠 Atualizações Recentes

## ✔ Sistema novo de UI

* Interface mais profissional
* Melhor organização
* Layout compacto
* Compatível com monitores menores

---

## ✔ Drag and Drop

Agora suporta:

* múltiplos vídeos
* importação rápida

---

## ✔ Motion Detection

Nova função experimental.

---

## ✔ Audio Threshold

Agora configurável pela interface.

---

## ✔ Margin Before / After

Separados individualmente.

---

## ✔ Progress Bar Real

Sem travamentos durante processamento.

---

## ✔ Sistema de Logs

Mais detalhado.

---

# ⚠ Possíveis Problemas

# FFmpeg não encontrado

Reinstale:

```text
install_auto_editor.bat
```

---

# Python não reconhecido

Feche e abra o Windows novamente após instalar.

---

# Thumbnail não aparece

O FFmpeg pode:

* não estar no PATH
* estar bloqueado
* não instalado corretamente

---

# 🛣 Roadmap Futuro

# 🎨 Melhorias Visuais

* tema claro
* mais animações
* timeline real
* preview player

---

# ⚡ Performance

* aceleração GPU
* processamento paralelo
* cache de thumbnails

---

# 🧠 Recursos Avançados

* AI Silence Detection
* AI Scene Detection
* Auto Zoom
* Auto Subtitle
* Auto Reframe

---

# 🐧 Versão Linux

O AutoCutStudio agora possui suporte experimental para Linux 🚀

Distribuições testadas:

```text
✔ Ubuntu
✔ Pop!_OS
✔ Linux Mint
✔ Fedora
✔ Arch Linux
```

---

# 📦 Formato Disponível

Atualmente o app é distribuído como:

```text
AppImage
```

O AppImage funciona como um executável portátil:

* não precisa instalar
* funciona em praticamente qualquer distro
* basta baixar e executar

---

# 📥 Como baixar

Baixe a versão Linux em:

```text
GitHub → Actions → Latest Build → Artifacts
```

ou futuramente na aba:

```text
Releases
```

---

# ▶ Como executar o AppImage

Depois de baixar:

## 1️⃣ Dar permissão de execução

```bash
chmod +x AutoCutStudio*.AppImage
```

---

## 2️⃣ Executar

```bash
./AutoCutStudio*.AppImage
```

---

# 🛠 Instalação Manual no Linux

Caso queira rodar pelo Python:

## Instalar dependências

Ubuntu / Debian:

```bash
sudo apt update

sudo apt install python3 python3-pip ffmpeg python3-tk -y
```

---

## Instalar bibliotecas Python

```bash
pip install -r requirements.txt
```

---

## Rodar o programa

```bash
python3 app.py
```

---

# 🧠 O que o AppImage inclui

```text
✔ Interface gráfica
✔ Auto-Editor
✔ Ícones Linux
✔ Sistema Drag & Drop
✔ Compatibilidade AppImage
✔ Integração KDE/GNOME
```

---

# ⚠ Possíveis Problemas no Linux

# AppImage não abre

Instale:

Ubuntu:

```bash
sudo apt install libfuse2
```

Fedora:

```bash
sudo dnf install fuse
```

Arch:

```bash
sudo pacman -S fuse2
```

---

# FFmpeg não encontrado

Instale:

Ubuntu:

```bash
sudo apt install ffmpeg
```

Arch:

```bash
sudo pacman -S ffmpeg
```

Fedora:

```bash
sudo dnf install ffmpeg
```

---

# Tkinter não encontrado

Ubuntu:

```bash
sudo apt install python3-tk
```

---

# Wayland Issues

Em alguns ambientes Wayland o Drag & Drop pode apresentar comportamento experimental.

Caso aconteça:

* use X11
* ou execute:

```bash
QT_QPA_PLATFORM=xcb
```

---

# 🛣 Futuro da versão Linux

Planejado:

```text
✔ Flatpak
✔ .deb
✔ Pacote Arch
✔ Instalador automático
✔ Repositórios oficiais
✔ Melhor integração GNOME/KDE
✔ Tema adaptativo
✔ Suporte Wayland completo
```

---

# ⚡ Build Automática Linux

O projeto possui CI/CD automático usando:

```text
GitHub Actions
```

Cada commit gera automaticamente:

```text
✔ Windows EXE
✔ Linux AppImage
```

---

# ❤️ Compatibilidade

O objetivo do projeto é manter suporte para:

```text
✔ Windows 10
✔ Windows 11
✔ Ubuntu
✔ Fedora
✔ Arch Linux
✔ Pop!_OS
✔ Linux Mint
```
# 🛡 Correções Futuras

Melhorias de compatibilidade:

* Windows 10
* Windows 11
* drivers antigos
* FFmpeg builds diferentes

---

# ❤️ Créditos

Powered by:

* Auto-Editor
* FFmpeg
* Python
* CustomTkinter

---

# ⭐ Contribuindo

Pull requests são bem-vindos.

Sugestões:

* melhorias de UI
* correções
* novas exportações
* novas automações
* tratar excessões de errors ao usar multlipas funções
* erros de ambiente 

---

# 📜 Licença

Creative Commons Legal Code

---

# 🔥 AutoCutStudio

```text
Effortless Automatic Video Editing
```
