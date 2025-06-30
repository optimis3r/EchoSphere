# 🎧 Echosphere

**Echosphere** is a Python-based audio enhancement tool that transforms regular stereo audio into an immersive experience. It features 8D rotation, bass boost, reverb, and binaural-style brainwave delay—all applied through FFmpeg. The app includes a simple GUI to guide users from input to enhanced output.

---

## ✨ Features

- 🎧 8D Audio Rotation (via FFmpeg `apulsator`)
- 🔊 Bass Boost with parametric EQ
- 🌫️ Reverb using echo filters
- 🧠 Binaural Delay (brainwave effect)
- 🖱️ GUI-based input/output selection
- 💽 Exports high-quality `.mp3` audio
- 📝 Output is automatically renamed to `originalfilename_enhanced.mp3`

---

## 🚀 Getting Started

---

### ✅ Requirements

- Python 3.7+
- [FFmpeg](https://ffmpeg.org/download.html) (must be in system PATH)
- Python packages:
  ```bash
  pip install pydub
### ▶️ Running the App

```bash
python src/echosphere.py
```

1. Select an input `.mp3`, `.wav`, or similar audio file.  
2. Choose which enhancements you want applied.  
3. Select where to save the final enhanced `.mp3` file.

---

## 📄 License

Licensed under the MIT License.

---

## ⚠️ Disclaimer

Do not upload or redistribute copyrighted material unless you have the appropriate rights.

---

## 🙌 Credits

- Built with [FFmpeg](https://ffmpeg.org/)
- Audio processing powered by [PyDub](https://github.com/jiaaro/pydub)
