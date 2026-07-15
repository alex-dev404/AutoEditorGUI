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
app.configure(bg="#101010")
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
    for video in video_paths:
        card = ctk.CTkFrame(scroll_frame, fg_color="#181818", corner_radius=16, height=105)
        card.pack(fill="x", padx=8, pady=8)

        thumb = gerar_thumbnail(video)
        if thumb:
            thumbnail_refs.append(thumb)
            ctk.CTkLabel(card, image=thumb, text="").pack(side="left", padx=10, pady=10)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10)

        nome = os.path.basename(video)
        ctk.CTkLabel(info_frame, text=nome, font=("Bahnschrift",22), anchor="w").pack(anchor="w", pady=(18,5))
        ctk.CTkLabel(info_frame, text="Pronto para processar", font=("Bahnschrift",15), text_color="#999").pack(anchor="w")

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

# =========================================
# INTERFACE INICIAL
# =========================================
header = ctk.CTkFrame(app, height=80, fg_color="#101010")
header.pack(fill="x", padx=10, pady=8)
logo = ctk.CTkLabel(header, text="AUTOCUTSTUDIO", font=("Impact",34))
logo.pack(side="left", padx=15)
status_label = ctk.CTkLabel(header, text="READY", font=("Bahnschrift",18), text_color="#00ff99")
status_label.pack(side="right", padx=20)

topbar = ctk.CTkFrame(app, fg_color="#161616", corner_radius=16, height=70)
topbar.pack(fill="x", padx=15, pady=5)
folder_button = ctk.CTkButton(topbar, text="Selecionar Pasta", command=escolher_pasta, font=("Bahnschrift",15), height=40, width=180)
folder_button.pack(side="left", padx=12, pady=12)

process_button = ctk.CTkButton(topbar, text="PROCESSAR", command=None, font=("Impact",20), fg_color="#0066ff", hover_color="#3385ff", width=220, height=44)
process_button.pack(side="right", padx=15)

folder_label = ctk.CTkLabel(app, text="Arraste vídeos aqui ou selecione uma pasta", font=("Bahnschrift",18), height=55, fg_color="#181818", corner_radius=14)
folder_label.pack(fill="x", padx=15, pady=8)
folder_label.drop_target_register(DND_FILES)
folder_label.dnd_bind("<<Drop>>", drop)

main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

left_panel = ctk.CTkFrame(main_frame, fg_color="#161616", corner_radius=18)
left_panel.pack(side="left", fill="both", expand=True, padx=(0,10))
scroll_frame = ctk.CTkScrollableFrame(left_panel, fg_color="transparent")
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

right_panel = ctk.CTkScrollableFrame(main_frame, width=320, fg_color="#161616", corner_radius=18)
right_panel.pack(side="right", fill="y")
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
export_title = ctk.CTkLabel(right_panel, text="EXPORT", font=("Impact",24))
export_title.pack(pady=(15,5))

export_option = ctk.StringVar(value="Resolve")
export_menu = ctk.CTkOptionMenu(
    right_panel,
    values=["Resolve","Premiere","Final Cut","Shotcut","Kdenlive"],
    variable=export_option,
    width=250,
    height=38,
    font=("Bahnschrift",15)
)
export_menu.pack(pady=5)

# SLIDER MARGIN
def atualizar_margin(valor): margin_value.configure(text=f"{valor:.2f} sec")
margin_title = ctk.CTkLabel(right_panel, text="Margin / Corte", font=("Bahnschrift",18))
margin_title.pack(pady=(20,3))
margin_slider = ctk.CTkSlider(right_panel, from_=0, to=2, number_of_steps=200, width=240, command=atualizar_margin)
margin_slider.set(config.get("margin",0.00))
margin_slider.pack()
margin_value = ctk.CTkLabel(right_panel, text=f"{margin_slider.get():.2f} sec", font=("Bahnschrift",15))
margin_value.pack()

# SLIDER THRESHOLD
def atualizar_threshold(valor): threshold_value.configure(text=f"-{valor:.0f} dB")
threshold_title = ctk.CTkLabel(right_panel, text="Audio Threshold", font=("Bahnschrift",18))
threshold_title.pack(pady=(20,3))
threshold_slider = ctk.CTkSlider(right_panel, from_=0, to=52, number_of_steps=52, width=240, command=atualizar_threshold)
threshold_slider.set(config.get("threshold",0))
threshold_slider.pack()
threshold_value = ctk.CTkLabel(right_panel, text=f"-{threshold_slider.get():.0f} dB", font=("Bahnschrift",15))
threshold_value.pack()

# SLIDER MOTION
def atualizar_motion(valor): motion_value.configure(text=f"{valor:.2f}")
motion_title = ctk.CTkLabel(right_panel, text="Motion Detection", font=("Bahnschrift",18))
motion_title.pack(pady=(20,3))
motion_slider = ctk.CTkSlider(right_panel, from_=0, to=1, number_of_steps=100, width=240, command=atualizar_motion)
motion_slider.set(config.get("motion",0))
motion_slider.pack()
motion_value = ctk.CTkLabel(right_panel, text=f"{motion_slider.get():.2f}", font=("Bahnschrift",15))
motion_value.pack()

# =========================================
# PROGRESS BAR
# =========================================
progress_bar = ctk.CTkProgressBar(right_panel, width=250, height=16)
progress_bar.pack(pady=25)
progress_bar.set(0)

# =========================================
# LOGS
# =========================================
logs_title = ctk.CTkLabel(right_panel, text="LOGS", font=("Impact",22))
logs_title.pack()
output_box = ctk.CTkTextbox(right_panel, width=260, height=180, font=("Consolas",12))
output_box.pack(padx=10, pady=10)

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
