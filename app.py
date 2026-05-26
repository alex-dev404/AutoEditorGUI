import os
import sys
import subprocess
import threading
import customtkinter as ctk

from tkinter import filedialog
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

# =========================================
# CONFIG
# =========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VIDEO_EXTENSIONS = [
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm"
]

video_paths = []
thumbnail_refs = []

# =========================================
# APP
# =========================================

app = TkinterDnD.Tk()

app.title("AutoCutStudio BY alex-dev404")
app.geometry("1280x760")
app.minsize(1000, 650)
app.configure(bg="#101010")
def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app.iconbitmap(
    resource_path("icon.ico")
)

# =========================================
# FONTS
# =========================================

TITLE_FONT = ("Impact", 34)
TEXT_FONT = ("Bahnschrift", 15)
SUBTITLE_FONT = ("Bahnschrift", 18)
BIG_FONT = ("Bahnschrift", 22)

# =========================================
# LOG
# =========================================

def log(texto):

    output_box.insert("end", f"{texto}\n")
    output_box.see("end")
    app.update()

# =========================================
# THUMBNAILS
# =========================================

def gerar_thumbnail(video_path):

    try:

        thumb_path = os.path.join(
            os.getcwd(),
            f"thumb_{abs(hash(video_path))}.jpg"
        )

        comando = (
            f'ffmpeg -y -ss 00:00:01 '
            f'-i "{video_path}" '
            f'-frames:v 1 '
            f'-q:v 2 '
            f'"{thumb_path}"'
        )

        subprocess.run(
            comando,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if os.path.exists(thumb_path):

            image = Image.open(thumb_path)

            image = image.resize((140, 80))

            thumb = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(140, 80)
            )

            return thumb

    except:
        return None

# =========================================
# UPDATE VIDEO LIST
# =========================================

def atualizar_lista_videos():

    global thumbnail_refs

    for widget in scroll_frame.winfo_children():
        widget.destroy()

    thumbnail_refs.clear()

    for video in video_paths:

        card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#181818",
            corner_radius=16,
            height=105
        )

        card.pack(
            fill="x",
            padx=8,
            pady=8
        )

        thumb = gerar_thumbnail(video)

        if thumb:

            thumbnail_refs.append(thumb)

            thumb_label = ctk.CTkLabel(
                card,
                image=thumb,
                text=""
            )

            thumb_label.pack(
                side="left",
                padx=10,
                pady=10
            )

        info_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        nome = os.path.basename(video)

        title = ctk.CTkLabel(
            info_frame,
            text=nome,
            font=BIG_FONT,
            anchor="w"
        )

        title.pack(
            anchor="w",
            pady=(18, 5)
        )

        subtitle = ctk.CTkLabel(
            info_frame,
            text="Pronto para processar",
            font=TEXT_FONT,
            text_color="#999999"
        )

        subtitle.pack(anchor="w")

# =========================================
# LOAD VIDEOS
# =========================================

def carregar_videos_pasta(pasta):

    video_paths.clear()

    for arquivo in os.listdir(pasta):

        caminho = os.path.join(
            pasta,
            arquivo
        )

        if any(
            arquivo.lower().endswith(ext)
            for ext in VIDEO_EXTENSIONS
        ):

            video_paths.append(caminho)

    atualizar_lista_videos()

# =========================================
# SELECT FOLDER
# =========================================

def escolher_pasta():

    pasta = filedialog.askdirectory()

    if not pasta:
        return

    folder_label.configure(
        text=pasta
    )

    carregar_videos_pasta(pasta)

# =========================================
# DRAG DROP
# =========================================

def drop(event):

    arquivos = app.tk.splitlist(event.data)

    for arquivo in arquivos:

        arquivo = arquivo.replace("{", "").replace("}", "")

        if os.path.isfile(arquivo):

            if any(
                arquivo.lower().endswith(ext)
                for ext in VIDEO_EXTENSIONS
            ):

                if arquivo not in video_paths:

                    video_paths.append(arquivo)

    atualizar_lista_videos()

# =========================================
# INSTALL DEPENDENCIES
# =========================================

def instalar_dependencias_thread():

    comandos = [
        "pip install auto-editor",
        "pip install ffmpeg-python",
        "pip install customtkinter",
        "pip install pillow",
        "pip install tkinterdnd2"
    ]

    total = len(comandos)

    progress_bar.set(0)

    for i, cmd in enumerate(comandos, start=1):

        status_label.configure(
            text=f"Instalando dependências ({i}/{total})"
        )

        log(f"\nExecutando:\n{cmd}\n")

        resultado = subprocess.run(
            cmd,
            shell=True
        )

        progress_bar.set(i / total)

        if resultado.returncode == 0:
            log("✅ Instalado")
        else:
            log("❌ Erro")

    status_label.configure(
        text="Dependências instaladas"
    )

def instalar_dependencias():

    threading.Thread(
        target=instalar_dependencias_thread,
        daemon=True
    ).start()

# =========================================
# PROCESS VIDEOS
# =========================================

def processar_videos_thread():

    if len(video_paths) == 0:

        log("Nenhum vídeo selecionado")
        return

    export_map = {
        "Resolve": "resolve",
        "Premiere": "premiere",
        "Final Cut": "final-cut-pro",
        "Shotcut": "shotcut",
        "Kdenlive": "kdenlive"
    }

    export_value = export_map[
        export_option.get()
    ]

    total = len(video_paths)

    progress_bar.set(0)

    for i, video in enumerate(video_paths, start=1):

        nome = os.path.basename(video)

        status_label.configure(
            text=f"Processando: {nome}"
        )

        # =========================================
        # OUTPUT NO MESMO LOCAL
        # =========================================

        pasta_video = os.path.dirname(video)

        nome_video = os.path.splitext(
            os.path.basename(video)
        )[0]

        ext_map = {
            "resolve": ".drt",
            "premiere": ".xml",
            "final-cut-pro": ".fcpxml",
            "shotcut": ".mlt",
            "kdenlive": ".kdenlive"
        }

        extensao = ext_map.get(
            export_value,
            ".xml"
        )

        arquivo_saida = os.path.join(
            pasta_video,
            nome_video + extensao
        )

        # =========================================
        # COMANDO
        # =========================================

        comando = (
            f'auto-editor "{video}" '
            f'--export {export_value} '
            f'--output "{arquivo_saida}" '
        )

        # =========================================
        # MARGIN NORMAL
        # =========================================

        margin = margin_slider.get()

        comando += (
            f'--margin {margin:.2f}sec '
        )

        # =========================================
        # MARGIN BEFORE / AFTER
        # =========================================

        margin_before = margin_before_slider.get()
        margin_after = margin_after_slider.get()

        if margin_before > 0 or margin_after > 0:

            comando += (
                f'--margin '
                f'{margin_before:.2f}sec,'
                f'{margin_after:.2f}sec '
            )

        # =========================================
        # PADDING
        # =========================================

        padding = padding_slider.get()

        if padding > 0:

            comando += (
                f'--cut-out '
                f'0,{padding:.2f}sec '
            )

        # =========================================
        # AUDIO THRESHOLD
        # =========================================

        threshold = threshold_slider.get()

        if threshold > 0:

            comando += (
                f'--edit audio:-{threshold:.0f}dB '
            )

        # =========================================
        # MOTION DETECTION
        # =========================================

        motion = motion_slider.get()

        if motion > 0:

            comando += (
                f'--edit motion:{motion:.2f} '
            )

        log(f"\nExecutando:\n{comando}\n")

        resultado = subprocess.run(
            comando,
            shell=True
        )

        if resultado.returncode == 0:

            log(f"✅ Finalizado: {nome}")

        else:

            log(f"❌ Erro: {nome}")

        progress_bar.set(i / total)

    status_label.configure(
        text="Todos os vídeos foram processados"
    )

def processar_videos():

    threading.Thread(
        target=processar_videos_thread,
        daemon=True
    ).start()

# =========================================
# UPDATE LABELS
# =========================================

def atualizar_margin(valor):
    margin_value.configure(
        text=f"{valor:.2f} sec"
    )

def atualizar_margin_before(valor):
    margin_before_value.configure(
        text=f"{valor:.2f} sec"
    )

def atualizar_margin_after(valor):
    margin_after_value.configure(
        text=f"{valor:.2f} sec"
    )

def atualizar_padding(valor):
    padding_value.configure(
        text=f"{valor:.2f} sec"
    )

def atualizar_threshold(valor):
    threshold_value.configure(
        text=f"-{valor:.0f} dB"
    )

def atualizar_motion(valor):
    motion_value.configure(
        text=f"{valor:.2f}"
    )

# =========================================
# HEADER
# =========================================

header = ctk.CTkFrame(
    app,
    height=80,
    fg_color="#101010"
)

header.pack(
    fill="x",
    padx=10,
    pady=8
)

logo = ctk.CTkLabel(
    header,
    text="AUTOCUTSTUDIO",
    font=TITLE_FONT
)

logo.pack(
    side="left",
    padx=15
)

status_label = ctk.CTkLabel(
    header,
    text="READY",
    font=SUBTITLE_FONT,
    text_color="#00ff99"
)

status_label.pack(
    side="right",
    padx=20
)

# =========================================
# TOPBAR
# =========================================

topbar = ctk.CTkFrame(
    app,
    fg_color="#161616",
    corner_radius=16,
    height=70
)

topbar.pack(
    fill="x",
    padx=15,
    pady=5
)

folder_button = ctk.CTkButton(
    topbar,
    text="Selecionar Pasta",
    command=escolher_pasta,
    font=TEXT_FONT,
    height=40,
    width=180
)

folder_button.pack(
    side="left",
    padx=12,
    pady=12
)

install_button = ctk.CTkButton(
    topbar,
    text="Instalar Dependências",
    command=instalar_dependencias,
    font=TEXT_FONT,
    fg_color="#008c55",
    hover_color="#00a865",
    height=40,
    width=210
)

install_button.pack(
    side="left",
    padx=8
)

process_button = ctk.CTkButton(
    topbar,
    text="PROCESSAR",
    command=processar_videos,
    font=("Impact", 20),
    fg_color="#0066ff",
    hover_color="#3385ff",
    width=220,
    height=44
)

process_button.pack(
    side="right",
    padx=15
)

# =========================================
# DROP AREA
# =========================================

folder_label = ctk.CTkLabel(
    app,
    text="Arraste vídeos aqui ou selecione uma pasta",
    font=SUBTITLE_FONT,
    height=55,
    fg_color="#181818",
    corner_radius=14
)

folder_label.pack(
    fill="x",
    padx=15,
    pady=8
)

folder_label.drop_target_register(DND_FILES)
folder_label.dnd_bind("<<Drop>>", drop)

# =========================================
# MAIN
# =========================================

main_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

# =========================================
# LEFT PANEL
# =========================================

left_panel = ctk.CTkFrame(
    main_frame,
    fg_color="#161616",
    corner_radius=18
)

left_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

scroll_frame = ctk.CTkScrollableFrame(
    left_panel,
    fg_color="transparent"
)

scroll_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================================
# RIGHT PANEL
# =========================================

right_panel = ctk.CTkScrollableFrame(
    main_frame,
    width=320,
    fg_color="#161616",
    corner_radius=18
)

right_panel.pack(
    side="right",
    fill="y"
)

# =========================================
# EXPORT
# =========================================

export_title = ctk.CTkLabel(
    right_panel,
    text="EXPORT",
    font=("Impact", 24)
)

export_title.pack(pady=(15, 5))

export_option = ctk.StringVar(
    value="Resolve"
)

export_menu = ctk.CTkOptionMenu(
    right_panel,
    values=[
        "Resolve",
        "Premiere",
        "Final Cut",
        "Shotcut",
        "Kdenlive"
    ],
    variable=export_option,
    width=250,
    height=38,
    font=TEXT_FONT
)

export_menu.pack(pady=5)

# =========================================
# MARGIN NORMAL
# =========================================

margin_title = ctk.CTkLabel(
    right_panel,
    text="Margin / Corte",
    font=SUBTITLE_FONT
)

margin_title.pack(pady=(20, 3))

margin_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=2,
    number_of_steps=200,
    width=240,
    command=atualizar_margin
)

margin_slider.set(0.20)

margin_slider.pack()

margin_value = ctk.CTkLabel(
    right_panel,
    text="0.20 sec",
    font=TEXT_FONT
)

margin_value.pack()

# =========================================
# MARGIN BEFORE
# =========================================

margin_before_title = ctk.CTkLabel(
    right_panel,
    text="Margin Before",
    font=SUBTITLE_FONT
)

margin_before_title.pack(pady=(20, 3))

margin_before_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=2,
    number_of_steps=200,
    width=240,
    command=atualizar_margin_before
)

margin_before_slider.set(0)

margin_before_slider.pack()

margin_before_value = ctk.CTkLabel(
    right_panel,
    text="0.00 sec",
    font=TEXT_FONT
)

margin_before_value.pack()

# =========================================
# MARGIN AFTER
# =========================================

margin_after_title = ctk.CTkLabel(
    right_panel,
    text="Margin After",
    font=SUBTITLE_FONT
)

margin_after_title.pack(pady=(20, 3))

margin_after_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=2,
    number_of_steps=200,
    width=240,
    command=atualizar_margin_after
)

margin_after_slider.set(0)

margin_after_slider.pack()

margin_after_value = ctk.CTkLabel(
    right_panel,
    text="0.00 sec",
    font=TEXT_FONT
)

margin_after_value.pack()

# =========================================
# PADDING
# =========================================

padding_title = ctk.CTkLabel(
    right_panel,
    text="Padding",
    font=SUBTITLE_FONT
)

padding_title.pack(pady=(20, 3))

padding_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=2,
    number_of_steps=200,
    width=240,
    command=atualizar_padding
)

padding_slider.set(0)

padding_slider.pack()

padding_value = ctk.CTkLabel(
    right_panel,
    text="0.00 sec",
    font=TEXT_FONT
)

padding_value.pack()

# =========================================
# THRESHOLD
# =========================================

threshold_title = ctk.CTkLabel(
    right_panel,
    text="Audio Threshold",
    font=SUBTITLE_FONT
)

threshold_title.pack(pady=(20, 3))

threshold_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=40,
    number_of_steps=40,
    width=240,
    command=atualizar_threshold
)

threshold_slider.set(0)

threshold_slider.pack()

threshold_value = ctk.CTkLabel(
    right_panel,
    text="-0 dB",
    font=TEXT_FONT
)

threshold_value.pack()

# =========================================
# MOTION
# =========================================

motion_title = ctk.CTkLabel(
    right_panel,
    text="Motion Detection",
    font=SUBTITLE_FONT
)

motion_title.pack(pady=(20, 3))

motion_slider = ctk.CTkSlider(
    right_panel,
    from_=0,
    to=1,
    number_of_steps=100,
    width=240,
    command=atualizar_motion
)

motion_slider.set(0)

motion_slider.pack()

motion_value = ctk.CTkLabel(
    right_panel,
    text="0.00",
    font=TEXT_FONT
)

motion_value.pack()

# =========================================
# PROGRESS BAR
# =========================================

progress_bar = ctk.CTkProgressBar(
    right_panel,
    width=250,
    height=16
)

progress_bar.pack(
    pady=25
)

progress_bar.set(0)

# =========================================
# LOGS
# =========================================

logs_title = ctk.CTkLabel(
    right_panel,
    text="LOGS",
    font=("Impact", 22)
)

logs_title.pack()

output_box = ctk.CTkTextbox(
    right_panel,
    width=260,
    height=180,
    font=("Consolas", 12)
)

output_box.pack(
    padx=10,
    pady=10
)

# =========================================
# LOOP
# =========================================

app.mainloop()
