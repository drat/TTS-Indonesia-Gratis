"""
████████╗████████╗███████╗
╚══██╔══╝╚══██╔══╝██╔════╝
   ██║      ██║   ███████╗
   ██║      ██║   ╚════██║
   ██║      ██║   ███████║
   ╚═╝      ╚═╝   ╚══════╝
██╗███╗   ██╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗██╗ █████╗ ██╗  ██╗██╗   ██╗
██║████╗  ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝██║██╔══██╗██║ ██╔╝██║   ██║
██║██╔██╗ ██║██║  ██║██║   ██║██╔██╗ ██║█████╗  ███████╗██║███████║█████╔╝ ██║   ██║
██║██║╚██╗██║██║  ██║██║   ██║██║╚██╗██║██╔══╝  ╚════██║██║██╔══██║██╔═██╗ ██║   ██║
██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚████║███████╗███████║██║██║  ██║██║  ██╗╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝

Script ini dibuat oleh __drat

Petunjuk:
1. Script ini digunakan untuk menghasilkan suara berbasis teks dengan berbagai pilihan pembicara.
2. Teknologi yang digunakan meliputi model text-to-speech (TTS) yang canggih dengan konversi teks ke fonem (G2P).
3. Model yang dipakai dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda.
4. Antarmuka dibuat dengan menggunakan Gradio dengan tema kustom bernama MetafisikTheme.

Cara Menggunakan:
1. Masukkan teks yang ingin diubah menjadi suara.
2. Pilih kecepatan bicara yang diinginkan.
3. Pilih bahasa dan pembicara yang diinginkan.
4. Klik tombol "Lakukan Inferensi Audio" untuk menghasilkan suara.
"""

import sys
import os
import json
import html
from uuid import uuid4
from time import sleep
from subprocess import run
import gradio as gr
import platform
from wget import download
import g2p_id
from themes import MetafisikTheme  # Impor tema custom dari themes.py
from g2p_id.scripts.tts import (
    g2p,
    config_file,
    model_file,
    model_url,
    cache_dir,
    text_normalization,
    )


speaker_mapping = {
    "Wibowo - Suara jantan berwibawa": "wibowo",
    "Ardi - Suara lembut dan hangat": "ardi",
    "Gadis - Suara perempuan yang merdu": "gadis",
    "Juminten - Suara perempuan jawa (bahasa jawa)": "JV-00264",
    "Asep - Suara lelaki sunda (bahasa sunda)": "SU-00060"
}

# Fullpath untuk command line tts
bin_dir = os.path.split(sys.executable)[0]
bin_tts = os.path.join(bin_dir, 'tts')

# Direktori untuk menyimpan file WAV yang terbentuk
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# File konfigurasi
data_dir = os.path.join(g2p_id.__path__[0], 'data')
config_base_file = os.path.join(data_dir, 'config.json')
speakers_file = os.path.join(data_dir, 'speakers.pth')
languages_file = os.path.join(data_dir, 'languages.json')


# Fungsi untuk mengecek apakah sistem operasi adalah macOS
def is_mac_os():
    return platform.system() == 'Darwin'


# Parameter default untuk konfigurasi
params = {
    "activate": True,
    "autoplay": True,
    "show_text": True,
    "remove_trailing_dots": False,
    "voice": "default.wav",
    "language": "Indonesian",
    "model_path": "checkpoint_1260000-inference.pth",
    "config_path": "config.json",
    "out_path": "output.wav"
}

SAMPLE_RATE = 16000
device = None

# Set nama pembicara default
default_speaker_name = "ardi"


# Fungsi untuk mengubah teks menjadi urutan yang sesuai untuk model
def text_to_sequence(text):
    # Implementasikan sesuai dengan kebutuhan model Anda
    # Sebagai contoh, ini adalah placeholder
    sequence = [ord(char) for char in text]
    return sequence


def create_filename(speaker):
    short_uuid = str(uuid4())[:8]
    return os.path.join(output_dir, f'{speaker}-{short_uuid}.wav')


# Fungsi untuk menghasilkan suara dengan progress bar
def gen_voice(text, speaker_label, speed, language, progress=gr.Progress()):
    speaker = speaker_mapping.get(speaker_label, default_speaker_name)
    progress(0, desc="Normalisasi teks dari HTML")
    text = html.unescape(text)
    sleep(2)
    progress(0.2, desc="Normalisasi teks agar bagus dibacanya")
    text = text_normalization(text)
    sleep(3)
    progress(0.4, desc="Ubah teks sesuai pengucapan")
    text_to_tts = g2p(text)
    if not os.path.exists(model_file):
        progress(0.5, desc="Unduh model bahasa sekitar 10 menit")
        download(model_url, out=cache_dir)
    output_file = create_filename(speaker)
    cmd = [bin_tts, '--text', text_to_tts,
           '--model_path', model_file,
           '--config_path', config_file,
           '--speaker_idx', speaker,
           '--out_path', output_file]
    progress(0.7, desc="Ubah menjadi file suara")
    result = run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    progress(1, desc="Selesai")
    sleep(2)
    return output_file


# Fungsi untuk memperbarui daftar pembicara
def update_speakers():
    speakers = [
        ("Wibowo - Suara jantan berwibawa", "wibowo"),
        ("Ardi - Suara lembut dan hangat", "ardi"),
        ("Gadis - Suara perempuan yang merdu", "gadis"),
        ("Juminten - Suara perempuan jawa (bahasa jawa)", "JV-00264"),
        ("Asep - Suara lelaki sunda (bahasa sunda)", "SU-00060")
    ]
    return speakers


# Fungsi untuk memperbarui dropdown pembicara
def update_dropdown(_=None, selected_speaker=default_speaker_name):
    choices = update_speakers()
    dropdown_choices = {label: label for label, value in choices}
    return gr.Dropdown(choices=dropdown_choices, value=selected_speaker, label="Pilih Pembicara", interactive=True, allow_custom_value=True)


# Memuat data bahasa
with open(languages_file, encoding='utf8') as f:
    languages = json.load(f)

# Antarmuka Gradio dengan tema MetafisikTheme
with gr.Blocks(theme=MetafisikTheme()) as app:

    gr.Markdown("### TTS Bahasa Indonesia", elem_id="main-title")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(lines=2, label="Teks", value="Halo, saya adalah pembicara virtual.", elem_id="text-input")
            speed_slider = gr.Slider(label='Kecepatan Bicara', minimum=0.1, maximum=1.99, value=0.8, step=0.01, elem_id="speed-slider")
            language_dropdown = gr.Dropdown(list(languages.keys()), label="Bahasa", value="Indonesian", elem_id="language-dropdown")
            submit_button = gr.Button("🗣️ Lakukan Inferensi Audio", elem_id="submit-button")
            explanation = gr.HTML("""
            <div style="margin-top: 20px; color: gray;">
                <h4>Kegunaan Aplikasi</h4>
                <p>Aplikasi ini digunakan untuk menghasilkan suara berbasis teks dengan berbagai pilihan pembicara.
                Teknologi yang digunakan meliputi model text-to-speech (TTS) yang canggih dengan konversi teks ke fonem.
                Model yang dipakai dilatih khusus untuk bahasa Indonesia, Jawa dan Sunda.</p>
                <h4>Cara Penggunaan</h4>
                <ol>
                    <li>Masukkan teks yang ingin diubah menjadi suara.</li>
                    <li>Pilih kecepatan bicara yang diinginkan.</li>
                    <li>Pilih bahasa dan pembicara yang diinginkan.</li>
                    <li>Klik tombol "Lakukan Inferensi Audio" untuk menghasilkan suara.</li>
                </ol>
                <p></p>
                <p>Semoga <b>Energi Semesta Digital</b> selalu bersama Anda!</p>
            </div>
            """)

        with gr.Column():
            with gr.Row():
                gr.Image("ardi.jpg", label="Ardi")
                gr.Image("gadis.jpg", label="Gadis")
                gr.Image("wibowo.jpg", label="Wibowo")

            speaker_dropdown = update_dropdown()
            refresh_button = gr.Button("👨‍👨‍👦 Segarkan Pembicara", elem_id="refresh-button")
            audio_output = gr.Audio(elem_id="audio-output")

            refresh_button.click(fn=update_dropdown, inputs=[], outputs=speaker_dropdown)

    submit_button.click(
        fn=gen_voice,
        inputs=[text_input, speaker_dropdown, speed_slider, language_dropdown],
        outputs=audio_output
    )

    gr.HTML("""
    <footer style="text-align: center; margin-top: 20px; color:silver;">
        Energi Semesta Digital © 2024 __drat. | 🇮🇩 Untuk Indonesia Jaya!
    </footer>
    """)

if __name__ == "__main__":
    app.launch()
