import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog

# =========================
# CONFIG
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================
# APP
# =========================

app = ctk.CTk()

app.title("Auto Editor GUI")
app.geometry("1100x700")

selected_folder = ""

# =========================
# FUNÇÕES
# =========================

def escolher_pasta():

    global selected_folder

    pasta = filedialog.askdirectory()

    if pasta:

        selected_folder = pasta

        folder_label.configure(
            text=pasta
        )

        carregar_videos()


def carregar_videos():

    video_list.delete("1.0", "end")

    if not selected_folder:
        return

    extensoes = [
        ".mp4",
        ".mov",
        ".avi",
        ".mkv"
    ]

    for arquivo in os.listdir(selected_folder):

        if any(
            arquivo.lower().endswith(ext)
            for ext in extensoes
        ):

            video_list.insert(
                "end",
                f"📹 {arquivo}\n"
            )


def instalar_dependencias():

    comandos = [
        "pip install auto-editor",
        "pip install ffmpeg-python"
    ]

    video_list.delete("1.0", "end")

    total = len(comandos)

    for i, cmd in enumerate(comandos, start=1):

        video_list.insert(
            "end",
            f"[{i}/{total}] INSTALANDO:\n{cmd}\n\n"
        )

        video_list.see("end")

        app.update()

        resultado = subprocess.run(
            cmd,
            shell=True
        )

        if resultado.returncode == 0:

            video_list.insert(
                "end",
                "✅ INSTALADO COM SUCESSO\n\n"
            )

        else:

            video_list.insert(
                "end",
                "❌ ERRO NA INSTALAÇÃO\n\n"
            )

        video_list.see("end")

        app.update()

    video_list.insert(
        "end",
        "\n🎉 TODAS AS DEPENDÊNCIAS FORAM INSTALADAS!\n"
    )

    output_box.insert(
        "end",
        "\nDependências instaladas!\n"
    )

    output_box.see("end")


def processar_videos():

    if not selected_folder:

        output_box.insert(
            "end",
            "\nSelecione uma pasta primeiro.\n"
        )

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

    margin = margin_slider.get()

    extensoes = [
        ".mp4",
        ".mov",
        ".avi",
        ".mkv"
    ]

    videos = []

    for arquivo in os.listdir(selected_folder):

        if any(
            arquivo.lower().endswith(ext)
            for ext in extensoes
        ):

            videos.append(arquivo)

    total = len(videos)

    if total == 0:

        output_box.insert(
            "end",
            "\nNenhum vídeo encontrado.\n"
        )

        return

    video_list.delete("1.0", "end")

    for i, arquivo in enumerate(videos, start=1):

        caminho = os.path.join(
            selected_folder,
            arquivo
        )

        video_list.insert(
            "end",
            f"[{i}/{total}] PROCESSANDO -> {arquivo}\n"
        )

        video_list.see("end")

        app.update()

        comando = (
            f'auto-editor "{caminho}" '
            f'--export {export_value} '
            f'--margin {margin:.2f}sec'
        )

        output_box.insert(
            "end",
            f"\nExecutando:\n{comando}\n"
        )

        output_box.see("end")

        app.update()

        resultado = subprocess.run(
            comando,
            shell=True
        )

        if resultado.returncode == 0:

            video_list.insert(
                "end",
                f"✅ FINALIZADO -> {arquivo}\n\n"
            )

        else:

            video_list.insert(
                "end",
                f"❌ ERRO -> {arquivo}\n\n"
            )

        video_list.see("end")

        app.update()

    video_list.insert(
        "end",
        "\n🎉 TODOS OS VÍDEOS FORAM PROCESSADOS!\n"
    )

    output_box.insert(
        "end",
        "\nProcessamento concluído!\n"
    )

    output_box.see("end")


def atualizar_margin(valor):

    margin_value.configure(
        text=f"{valor:.2f} sec"
    )

# =========================
# TÍTULO
# =========================

title = ctk.CTkLabel(
    app,
    text="AUTO EDITOR GUI",
    font=("Segoe UI", 30, "bold")
)

title.pack(pady=20)

# =========================
# BOTÃO PASTA
# =========================

folder_button = ctk.CTkButton(
    app,
    text="Selecionar Pasta",
    command=escolher_pasta,
    width=250,
    height=40
)

folder_button.pack(pady=10)

folder_label = ctk.CTkLabel(
    app,
    text="Nenhuma pasta selecionada"
)

folder_label.pack()

# =========================
# LISTA DE VÍDEOS
# =========================

video_frame = ctk.CTkFrame(app)

video_frame.pack(
    fill="both",
    expand=False,
    padx=20,
    pady=20
)

video_list = ctk.CTkTextbox(
    video_frame,
    height=200
)

video_list.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# =========================
# MARGIN
# =========================

timeline_label = ctk.CTkLabel(
    app,
    text="Margin / Corte",
    font=("Segoe UI", 20, "bold")
)

timeline_label.pack(pady=10)

margin_slider = ctk.CTkSlider(
    app,
    from_=0,
    to=2,
    number_of_steps=200,
    width=600,
    command=atualizar_margin
)

margin_slider.set(0.05)

margin_slider.pack(pady=10)

margin_value = ctk.CTkLabel(
    app,
    text="0.05 sec"
)

margin_value.pack()

# =========================
# EXPORT MENU
# =========================

export_option = ctk.StringVar(
    value="Resolve"
)

export_menu = ctk.CTkOptionMenu(
    app,
    values=[
        "Resolve",
        "Premiere",
        "Final Cut",
        "Shotcut",
        "Kdenlive"
    ],
    variable=export_option,
    width=300
)

export_menu.pack(pady=20)

# =========================
# BOTÕES
# =========================

button_frame = ctk.CTkFrame(app)

button_frame.pack(pady=20)

install_button = ctk.CTkButton(
    button_frame,
    text="Instalar Dependências",
    command=instalar_dependencias,
    fg_color="green",
    width=220
)

install_button.grid(
    row=0,
    column=0,
    padx=10
)

process_button = ctk.CTkButton(
    button_frame,
    text="Processar Vídeos",
    command=processar_videos,
    width=220
)

process_button.grid(
    row=0,
    column=1,
    padx=10
)

# =========================
# OUTPUT
# =========================

output_box = ctk.CTkTextbox(
    app,
    height=180
)

output_box.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

# =========================
# LOOP
# =========================

app.mainloop()