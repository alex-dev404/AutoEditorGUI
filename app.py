import os, sys, subprocess, threading, json, logging
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

# =========================================
# CONFIGURAÇÃO
# =========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

VIDEO_EXTENSIONS = [".mp4",".mov",".avi",".mkv",".webm"]
video_paths, thumbnail_refs = [], []
CONFIG_FILE = "config.json"
FONT = "Inter"
ACCENT = "#2563EB"
ACCENT_HOVER = "#1D4ED8"
THEMES = {
    "dark": {
        "app": "#0F1115", "surface": "#171A21", "surface_2": "#20242D",
        "input": "#252A34", "text": "#F8FAFC", "muted": "#9AA4B2",
        "border": "#303744", "drop": "#172A4D", "log": "#0B0D11",
    },
    "light": {
        "app": "#F4F6F8", "surface": "#FFFFFF", "surface_2": "#EEF2F6",
        "input": "#E7ECF2", "text": "#18212F", "muted": "#637083",
        "border": "#D5DDE7", "drop": "#E3EDFF", "log": "#16202E",
    },
}

# Logging para arquivo + console
logging.basicConfig(
    filename="autocutstudio.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    output_box.insert("end", f"{msg}\n")
    output_box.see("end")
    app.update()
    logging.info(msg)

# =========================================
# CONFIGURAÇÕES PERSISTENTES
# =========================================
def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE,"r") as f:
            return json.load(f)
    return {}

def salvar_config(cfg):
    with open(CONFIG_FILE,"w") as f:
        json.dump(cfg,f,indent=2)

config = carregar_config()
theme_name = config.get("theme", "dark") if config.get("theme") in THEMES else "dark"

# =========================================
# RESOURCE PATH
# =========================================
def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =========================================
# APP
# =========================================
app = TkinterDnD.Tk()
app.title("AutoCutStudio BY alex-dev404")
app.geometry("1280x760")
app.minsize(1000,650)
try: app.iconbitmap(resource_path("icon.ico"))
except: pass
try: app.iconphoto(True, tk.PhotoImage(file=resource_path("icon.png")))
except: pass
app.configure(bg=THEMES[theme_name]["app"])

def current_theme():
    return THEMES[theme_name]

def set_theme(name=None):
    global theme_name
    theme_name = name or ("light" if theme_name == "dark" else "dark")
    colors = current_theme()
    ctk.set_appearance_mode(theme_name)
    app.configure(bg=colors["app"])
    for widget, options in theme_widgets:
        resolved = {key: value() if callable(value) else value for key, value in options.items()}
        widget.configure(**{key: value for key, value in resolved.items() if value is not None})
    atualizar_cores_lista_videos()
    theme_button.configure(text="☀  Modo claro" if theme_name == "dark" else "☾  Modo escuro")
    config["theme"] = theme_name
    salvar_config(config)

theme_widgets = []
video_cards = []

def themed(widget, **options):
    theme_widgets.append((widget, options))
    return widget

def atualizar_cores_lista_videos():
    colors = current_theme()
    scroll_frame.configure(fg_color=colors["surface"])
    for card, name_label, status in video_cards:
        card.configure(fg_color=colors["surface_2"])
        name_label.configure(text_color=colors["text"])
        status.configure(text_color=colors["muted"])
# =========================================
# THUMBNAILS
# =========================================
def gerar_thumbnail(video_path):
    try:
        thumb_path = os.path.join(os.getcwd(), f"thumb_{abs(hash(video_path))}.jpg")
        comando = f'ffmpeg -y -ss 00:00:01 -i "{video_path}" -frames:v 1 -q:v 2 "{thumb_path}"'
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(thumb_path):
            image = Image.open(thumb_path).resize((140,80))
            thumb = ctk.CTkImage(light_image=image, dark_image=image, size=(140,80))
            return thumb
    except Exception as e:
        logging.error(f"Erro ao gerar thumbnail: {e}")
    return None

# =========================================
# LISTA DE VÍDEOS
# =========================================
def atualizar_lista_videos():
    global thumbnail_refs
    for w in scroll_frame.winfo_children():
        w.destroy()
    thumbnail_refs.clear()
    video_cards.clear()
    for video in video_paths:
        colors = current_theme()
        card = ctk.CTkFrame(scroll_frame, fg_color=colors["surface_2"], corner_radius=10, height=105)
        card.pack(fill="x", padx=8, pady=8)

        thumb = gerar_thumbnail(video)
        if thumb:
            thumbnail_refs.append(thumb)
            ctk.CTkLabel(card, image=thumb, text="").pack(side="left", padx=10, pady=10)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)

        nome = os.path.basename(video)
        name_label = ctk.CTkLabel(info_frame, text=nome, font=(FONT, 18, "bold"), text_color=colors["text"], anchor="w")
        name_label.pack(anchor="w", pady=(18,5))
        status = ctk.CTkLabel(info_frame, text="Pronto para processar", font=(FONT, 13), text_color=colors["muted"])
        status.pack(anchor="w")
        video_cards.append((card, name_label, status))

# =========================================
# CARREGAR VÍDEOS
# =========================================
def carregar_videos_pasta(pasta):
    video_paths.clear()
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if any(arquivo.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
            video_paths.append(caminho)
    atualizar_lista_videos()
    config["ultima_pasta"] = pasta
    salvar_config(config)

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        folder_label.configure(text=pasta)
        carregar_videos_pasta(pasta)

def drop(event):
    arquivos = app.tk.splitlist(event.data)
    for arquivo in arquivos:
        arquivo = arquivo.replace("{","").replace("}","")
        if os.path.isfile(arquivo) and any(arquivo.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
            if arquivo not in video_paths:
                video_paths.append(arquivo)
    atualizar_lista_videos()
    folder_label.configure(fg_color=current_theme()["surface_2"], text_color=current_theme()["muted"])

# =========================================
# INTERFACE INICIAL
# =========================================
header = themed(ctk.CTkFrame(app, height=72, fg_color=None), fg_color=lambda: current_theme()["app"])
header.pack(fill="x", padx=10, pady=8)
logo = themed(ctk.CTkLabel(header, text="AUTOCUTSTUDIO", font=(FONT, 27, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
logo.pack(side="left", padx=15)
status_label = themed(ctk.CTkLabel(header, text="READY", font=(FONT, 12, "bold"), text_color="#22C55E"), text_color="#22C55E")
status_label.pack(side="right", padx=(18, 12))
theme_button = themed(ctk.CTkButton(header, text="☀  Modo claro" if theme_name == "dark" else "☾  Modo escuro", command=set_theme, width=145, height=32, corner_radius=9, font=(FONT, 12), fg_color=None, hover_color=ACCENT, text_color=None), fg_color=lambda: current_theme()["surface_2"], text_color=lambda: current_theme()["text"])
theme_button.pack(side="right", padx=8)

topbar = themed(ctk.CTkFrame(app, fg_color=None, corner_radius=12, height=66), fg_color=lambda: current_theme()["surface"])
topbar.pack(fill="x", padx=15, pady=5)
folder_button = ctk.CTkButton(topbar, text="Selecionar pasta", command=escolher_pasta, font=(FONT, 13), height=38, width=180, corner_radius=9, fg_color=ACCENT, hover_color=ACCENT_HOVER)
folder_button.pack(side="left", padx=12, pady=12)

process_button = ctk.CTkButton(topbar, text="PROCESSAR VÍDEOS", command=None, font=(FONT, 14, "bold"), fg_color="#16A34A", hover_color="#15803D", width=220, height=40, corner_radius=9)
process_button.pack(side="right", padx=15)

folder_label = themed(ctk.CTkLabel(app, text="＋  Arraste vídeos aqui ou selecione uma pasta", font=(FONT, 15), height=54, fg_color=None, text_color=None, corner_radius=10), fg_color=lambda: current_theme()["surface_2"], text_color=lambda: current_theme()["muted"])
folder_label.pack(fill="x", padx=15, pady=8)
folder_label.drop_target_register(DND_FILES)
folder_label.dnd_bind("<<Drop>>", drop)
folder_label.dnd_bind("<<DragEnter>>", lambda event: folder_label.configure(fg_color=current_theme()["drop"], text_color=ACCENT))
folder_label.dnd_bind("<<DragLeave>>", lambda event: folder_label.configure(fg_color=current_theme()["surface_2"], text_color=current_theme()["muted"]))

main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=15, pady=10)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_rowconfigure(0, weight=1)

left_panel = themed(ctk.CTkFrame(main_frame, fg_color=None, corner_radius=12), fg_color=lambda: current_theme()["surface"])
left_panel.grid(row=0, column=0, sticky="nsew", padx=(0,10))
scroll_frame = themed(ctk.CTkScrollableFrame(left_panel, fg_color=None), fg_color=lambda: current_theme()["surface"])
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

right_panel = themed(ctk.CTkScrollableFrame(main_frame, width=320, fg_color=None, corner_radius=12), fg_color=lambda: current_theme()["surface"])
right_panel.grid(row=0, column=1, sticky="nsew")
# =========================================
# PROCESSAR VÍDEOS
# =========================================
def processar_videos_thread():
    if not video_paths:
        log("Nenhum vídeo selecionado")
        return

    process_button.configure(state="disabled")
    export_map = {
        "Resolve": "resolve",
        "Premiere": "premiere",
        "Final Cut": "final-cut-pro",
        "Shotcut": "shotcut",
        "Kdenlive": "kdenlive"
    }
    export_value = export_map[export_option.get()]
    total = len(video_paths)
    progress_bar.set(0)

    for i, video in enumerate(video_paths, 1):
        nome = os.path.basename(video)
        status_label.configure(text=f"Processando: {nome}")

        pasta_video = os.path.dirname(video)
        nome_video = os.path.splitext(nome)[0]
        ext_map = {
            "resolve": ".drt",
            "premiere": ".xml",
            "final-cut-pro": ".fcpxml",
            "shotcut": ".mlt",
            "kdenlive": ".kdenlive"
        }
        arquivo_saida = os.path.join(pasta_video, nome_video + ext_map.get(export_value, ".xml"))

        comando = f'python3 -m auto_editor "{video}" --export {export_value} --output "{arquivo_saida}" '
        comando += f'--margin {margin_slider.get():.2f}sec '

        log(f"\nExecutando:\n{comando}\n")
        resultado = subprocess.run(comando, shell=True)

        if resultado.returncode == 0:
            log(f"✅ Finalizado: {nome}")
        else:
            log(f"❌ Erro: {nome}")

        progress_bar.set(i/total)

    status_label.configure(text="Todos os vídeos foram processados")
    process_button.configure(state="normal")

def processar_videos():
    threading.Thread(target=processar_videos_thread, daemon=True).start()

# =========================================
# PAINEL DIREITO
# =========================================
export_title = themed(ctk.CTkLabel(right_panel, text="EXPORTAÇÃO", font=(FONT, 20, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
export_title.pack(pady=(15,5))

export_option = ctk.StringVar(value="Resolve")
export_menu = ctk.CTkOptionMenu(
    right_panel,
    values=["Resolve","Premiere","Final Cut","Shotcut","Kdenlive"],
    variable=export_option,
    width=250,
    height=38,
    font=(FONT, 13), fg_color=ACCENT, button_color=ACCENT, button_hover_color=ACCENT_HOVER
)
export_menu.pack(pady=5)

# SLIDER MARGIN
def atualizar_margin(valor): margin_value.configure(text=f"{valor:.2f} sec")
margin_title = themed(ctk.CTkLabel(right_panel, text="Margem de corte", font=(FONT, 14, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
margin_title.pack(pady=(20,3))
margin_slider = ctk.CTkSlider(right_panel, from_=0, to=2, number_of_steps=200, width=240, command=atualizar_margin)
margin_slider.set(config.get("margin",0.00))
margin_slider.pack()
margin_value = themed(ctk.CTkLabel(right_panel, text=f"{margin_slider.get():.2f} sec", font=(FONT, 12), text_color=None), text_color=lambda: current_theme()["muted"])
margin_value.pack()

# SLIDER THRESHOLD
def atualizar_threshold(valor): threshold_value.configure(text=f"-{valor:.0f} dB")
threshold_title = themed(ctk.CTkLabel(right_panel, text="Limite de áudio", font=(FONT, 14, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
threshold_title.pack(pady=(20,3))
threshold_slider = ctk.CTkSlider(right_panel, from_=0, to=52, number_of_steps=52, width=240, command=atualizar_threshold)
threshold_slider.set(config.get("threshold",0))
threshold_slider.pack()
threshold_value = themed(ctk.CTkLabel(right_panel, text=f"-{threshold_slider.get():.0f} dB", font=(FONT, 12), text_color=None), text_color=lambda: current_theme()["muted"])
threshold_value.pack()

# SLIDER MOTION
def atualizar_motion(valor): motion_value.configure(text=f"{valor:.2f}")
motion_title = themed(ctk.CTkLabel(right_panel, text="Detecção de movimento", font=(FONT, 14, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
motion_title.pack(pady=(20,3))
motion_slider = ctk.CTkSlider(right_panel, from_=0, to=1, number_of_steps=100, width=240, command=atualizar_motion)
motion_slider.set(config.get("motion",0))
motion_slider.pack()
motion_value = themed(ctk.CTkLabel(right_panel, text=f"{motion_slider.get():.2f}", font=(FONT, 12), text_color=None), text_color=lambda: current_theme()["muted"])
motion_value.pack()

# =========================================
# PROGRESS BAR
# =========================================
progress_bar = ctk.CTkProgressBar(right_panel, width=250, height=12, progress_color=ACCENT)
progress_bar.pack(pady=25)
progress_bar.set(0)

# =========================================
# LOGS
# =========================================
logs_title = themed(ctk.CTkLabel(right_panel, text="ATIVIDADE", font=(FONT, 15, "bold"), text_color=None), text_color=lambda: current_theme()["text"])
logs_title.pack()
output_box = themed(ctk.CTkTextbox(right_panel, width=260, height=180, font=("DejaVu Sans Mono", 11), fg_color=None, text_color="#E2E8F0", border_width=1, border_color=None, corner_radius=8), fg_color=lambda: current_theme()["log"], border_color=lambda: current_theme()["border"])
output_box.pack(padx=10, pady=10)

set_theme(theme_name)

# Conectar botão PROCESSAR
process_button.configure(command=processar_videos)
# =========================================
# CARREGAR ÚLTIMA PASTA
# =========================================
if "ultima_pasta" in config:
    folder_label.configure(text=config["ultima_pasta"])
    carregar_videos_pasta(config["ultima_pasta"])

# =========================================
# SALVAR CONFIGURAÇÕES AO FECHAR
# =========================================
def salvar_configuracoes():
    config["margin"] = margin_slider.get()
    config["threshold"] = threshold_slider.get()
    config["motion"] = motion_slider.get()
    salvar_config(config)

    app.destroy()

app.protocol("WM_DELETE_WINDOW", salvar_configuracoes)

# =========================================
# LOOP PRINCIPAL
# =========================================
app.mainloop()
