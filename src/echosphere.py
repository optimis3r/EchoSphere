import io
import os
import subprocess
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------- Audio Processing ----------
def apply_ffmpeg_filter(audio: AudioSegment, filter_str: str) -> AudioSegment:
    buf = io.BytesIO()
    audio.export(buf, format="wav")
    buf.seek(0)

    process = subprocess.run(
        ['ffmpeg', '-y', '-i', 'pipe:0', '-af', filter_str, '-f', 'wav', 'pipe:1'],
        input=buf.read(),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    return AudioSegment.from_file(io.BytesIO(process.stdout), format="wav")

def add_reverb(audio: AudioSegment) -> AudioSegment:
    return apply_ffmpeg_filter(audio, "aecho=0.6:0.5:40:0.25")

def add_bass_boost(audio: AudioSegment, gain_db=15) -> AudioSegment:
    return apply_ffmpeg_filter(audio, f"equalizer=f=90:t=q:w=2:g={gain_db}")

def add_brainwave_effect(audio: AudioSegment, delay_ms=15) -> AudioSegment:
    left, right = audio.split_to_mono()
    delayed_right = AudioSegment.silent(duration=delay_ms) + right
    min_len = min(len(left), len(delayed_right))
    return AudioSegment.from_mono_audiosegments(left[:min_len], delayed_right[:min_len])

def apply_8d_effect(audio: AudioSegment, spin_speed=0.2) -> AudioSegment:
    return apply_ffmpeg_filter(audio, f"apulsator=hz={spin_speed}")

# ---------- GUI ----------
class Audio8DApp:
    def __init__(self, root):
        self.root = root
        self.file_path = None

        root.title("🎧 Enhanced 8D Audio Converter")
        root.geometry("460x350")
        root.configure(bg="#1e1e1e")

        button_bg = "#2e2e2e"
        button_fg = "white"
        button_hover = "#444444"
        checkbox_fg = "white"
        checkbox_bg = "#1e1e1e"
        checkbox_active = "#3e3e3e"

        tk.Label(root, text="Select Audio File", bg=checkbox_bg, fg=checkbox_fg, font=("Segoe UI", 11)).pack(pady=(20, 5))
        self.browse_btn = tk.Button(root, text="Browse", command=self.select_file, bg=button_bg, fg=button_fg,
                                    activebackground=button_hover, activeforeground=button_fg, relief="flat")
        self.browse_btn.pack(pady=(0, 15))

        self.status = tk.Label(root, text="", bg=checkbox_bg, fg=checkbox_fg, font=("Segoe UI", 10))
        self.status.pack(pady=(0, 10))

        self.var_bass = tk.BooleanVar()
        self.var_reverb = tk.BooleanVar()
        self.var_brain = tk.BooleanVar()

        for text, var in [
            ("Bass Boost", self.var_bass),
            ("Reverb", self.var_reverb),
            ("Brainwave Effect", self.var_brain),
        ]:
            cb = tk.Checkbutton(
                root, text=text, variable=var,
                font=("Segoe UI", 10), bg=checkbox_bg, fg=checkbox_fg,
                activebackground=checkbox_active, activeforeground=checkbox_fg,
                selectcolor="#222222", relief="flat", anchor="w"
            )
            cb.pack(pady=2)

        self.process_btn = tk.Button(
            root, text="Process & Export", command=self.process_audio,
            bg=button_bg, fg=button_fg,
            activebackground=button_hover, activeforeground=button_fg,
            relief="flat", padx=10, pady=5
        )
        self.process_btn.pack(pady=(20, 10))

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")])
        if path:
            self.file_path = path
            self.status.config(text=f"Selected: {os.path.basename(path)}")
        else:
            self.status.config(text="❌ No file selected")

    def process_audio(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select an audio file.")
            return

        try:
            self.status.config(text="⏳ Processing...")
            self.root.update()

            audio = AudioSegment.from_file(self.file_path).set_channels(2)
            audio = apply_8d_effect(audio)

            if self.var_bass.get():
                audio = add_bass_boost(audio)
            if self.var_reverb.get():
                audio = add_reverb(audio)
            if self.var_brain.get():
                audio = add_brainwave_effect(audio)

            # Get original filename without extension
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            default_name = f"{base_name}_enhanced.mp3"

            export_path = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                initialfile=default_name,
                filetypes=[("MP3 Files", "*.mp3")]
            )

            if not export_path:
                self.status.config(text="❌ Export cancelled.")
                return

            audio.export(export_path, format="mp3", bitrate="320k")
            self.status.config(text=f"✅ Exported to: {os.path.basename(export_path)}")

        except Exception as e:
            self.status.config(text=f"❌ Error: {e}")

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = Audio8DApp(root)
    root.mainloop()
