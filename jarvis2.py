import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading, time, os, webbrowser, subprocess, datetime

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import wikipedia
except ImportError:
    wikipedia = None

# Check PyAudio availability
try:
    import pyaudio
    pyaudio_ok = True
except ImportError:
    pyaudio_ok = False


APP_TITLE = "Jarvis Assistant"
DEFAULT_RATE = 175


class JarvisGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title(APP_TITLE)
        root.geometry("820x600")
        root.minsize(760, 560)

        # ---- TTS engine ----
        self.engine = pyttsx3.init() if pyttsx3 else None
        if self.engine:
            self.voices = self.engine.getProperty("voices")
            self.engine.setProperty("rate", DEFAULT_RATE)

        # ---- State ----
        self.listening = False
        self.listen_thread = None
        self.speaking_enabled = tk.BooleanVar(value=True)

        # ---- Build UI ----
        self._build_header()
        self._build_controls()
        self._build_log()
        self._build_input()

        # Init voice list
        self._populate_voices()

        # Show capability status
        if sr is None:
            self._log("⚠️ SpeechRecognition not available. Voice input disabled.")
        elif not pyaudio_ok:
            self._log("⚠️ PyAudio not found. Voice input disabled. (Typed commands still work.)")

        self._update_mic_button_state()

    # ---------- UI ----------
    def _build_header(self):
        header = ttk.Frame(self.root, padding=6)
        header.pack(fill="x")

        ttk.Label(header, text="Jarvis Assistant 🤖", font=("Segoe UI", 18, "bold")).pack(side="left")

        right = ttk.Frame(header)
        right.pack(side="right")

        chk = ttk.Checkbutton(right, text="Speak replies", variable=self.speaking_enabled)
        chk.pack(side="left", padx=4)

        ttk.Label(right, text="Voice:").pack(side="left")
        self.voice_combo = ttk.Combobox(right, width=18, state="readonly")
        self.voice_combo.pack(side="left", padx=2)
        self.voice_combo.bind("<<ComboboxSelected>>", self._on_voice_change)

    def _build_controls(self):
        controls = ttk.Frame(self.root, padding=6)
        controls.pack(fill="x")

        self.mic_btn = ttk.Button(controls, text="🎙 Speak", command=self._on_mic_click)
        self.mic_btn.pack(side="left")

        self.stop_btn = ttk.Button(controls, text="⏹ Stop", command=self._on_stop, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

    def _build_log(self):
        frame = ttk.Frame(self.root, padding=6)
        frame.pack(fill="both", expand=True)

        self.log = scrolledtext.ScrolledText(frame, wrap="word", font=("Consolas", 11))
        self.log.pack(fill="both", expand=True)

    def _build_input(self):
        frame = ttk.Frame(self.root, padding=6)
        frame.pack(fill="x")

        self.entry = ttk.Entry(frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self.on_send_click())

        send_btn = ttk.Button(frame, text="Send", command=self.on_send_click)
        send_btn.pack(side="right")

    # ---------- Events ----------
    def _on_voice_change(self, event=None):
        if not self.engine: return
        idx = self.voice_combo.current()
        if idx >= 0:
            self.engine.setProperty("voice", self.voices[idx].id)

    def _on_mic_click(self):
        if self.listening or not sr: return
        self.listening = True
        self.mic_btn.config(text="Listening...", state="disabled")
        self.listen_thread = threading.Thread(target=self._listen_once_thread, daemon=True)
        self.listen_thread.start()

    def _on_stop(self):
        if self.engine: self.engine.stop()
        self.stop_btn.config(state="disabled")

    def on_send_click(self):
        text = self.entry.get().strip()
        if not text: return
        self._log(f"👤 You: {text}")
        self.entry.delete(0, tk.END)
        self._handle_command_async(text)

    # ---------- Log ----------
    def _log(self, text: str):
        self.log.insert("end", text + "\n")
        self.log.see("end")

    # ---------- Threads ----------
    def _listen_once_thread(self):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self._log("🎙 Listening…")
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)

            try:
                text = recognizer.recognize_google(audio)
                text = text.strip()
                self._log(f"👤 You (voice): {text}")
                self._handle_command_async(text)
            except sr.UnknownValueError:
                self._log("🤖 Jarvis: Sorry, I didn’t catch that.")
                self._say("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                self._log(f"🤖 Jarvis: Network error: {e}")
                self._say("Network error.")
        except Exception as e:
            self._log(f"⚠️ Mic error: {e}")
        finally:
            self.listening = False
            self.mic_btn.config(text="🎙 Speak", state="normal" if pyaudio_ok and (sr is not None) else "disabled")

    def _handle_command_async(self, text: str):
        t = threading.Thread(target=self._handle_command, args=(text,), daemon=True)
        t.start()

    # ---------- Command Handling ----------
    def _handle_command(self, command: str):
        cmd = command.lower().strip()
        reply = None

        # --- Exit ---
        if cmd in ["exit", "quit", "bye"]:
            self._say("Goodbye!")
            self.root.quit()
            return

        # --- Time ---
        if "time" in cmd:
            now = datetime.datetime.now().strftime("%H:%M")
            reply = f"The time is {now}."
            self._log(f"🤖 Jarvis: {reply}")
            self._say(reply)
            return

        # --- Google Search ---
        if cmd.startswith("search ") and " on google" in cmd:
            query = cmd.replace("search ", "").replace(" on google", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                reply = f"Searching {query} on Google."
                self._log(f"🤖 Jarvis: {reply}")
                self._say(reply)
            return

        # --- YouTube Search ---
        if cmd.startswith("search ") and " on youtube" in cmd:
            query = cmd.replace("search ", "").replace(" on youtube", "").strip()
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                reply = f"Searching {query} on YouTube."
                self._log(f"🤖 Jarvis: {reply}")
                self._say(reply)
            return

        # --- YouTube Play ---
        if cmd.startswith("play "):
            song = cmd.replace("play ", "")
            url = f"https://www.youtube.com/results?search_query={song}"
            webbrowser.open(url)
            reply = f"Playing {song} on YouTube."
            self._log(f"🤖 Jarvis: {reply}")
            self._say(reply)
            return

        # --- Fixed Sites ---
        if "open youtube" in cmd:
            webbrowser.open("https://youtube.com"); reply="Opening YouTube."
        elif "open google" in cmd:
            webbrowser.open("https://google.com"); reply="Opening Google."
        elif "open github" in cmd:
            webbrowser.open("https://github.com"); reply="Opening GitHub."
        elif "open instagram" in cmd:
            webbrowser.open("https://instagram.com"); reply="Opening Instagram."

        # --- Apps on PC ---
        elif cmd.startswith("open "):
            app_name = cmd.replace("open ", "").strip()
            try:
                os.startfile(app_name)  # works if app in PATH or Windows knows
                reply = f"Opening {app_name}."
            except Exception:
                reply = f"Sorry, I couldn't open {app_name}."

        # --- Wikipedia ---
        elif cmd.startswith("who is") or cmd.startswith("what is"):
            if wikipedia:
                try:
                    topic = command.split(" ", 2)[-1]
                    summary = wikipedia.summary(topic, sentences=2)
                    reply = summary
                except Exception:
                    reply = "I couldn't fetch information right now."
            else:
                reply = "Wikipedia module not available."

        # --- Help ---
        elif cmd == "help":
            reply = (
                "Commands:\n"
                "- play <song> (YouTube)\n"
                "- search <query> on google\n"
                "- search <query> on youtube\n"
                "- open <app/site>\n"
                "- who is / what is <topic>\n"
                "- time\n"
                "- exit\n"
            )

        # --- Unknown ---
        else:
            reply = "I don't know how to handle that."

        # --- Speak + Log ---
        if reply:
            self._log(f"🤖 Jarvis: {reply}")
            self._say(reply)

    # ---------- TTS ----------
    def _say(self, text: str):
        if not self.engine or not self.speaking_enabled.get(): return
        self.stop_btn.config(state="normal")
        self.engine.say(text)
        self.engine.runAndWait()
        self.stop_btn.config(state="disabled")

    # ---------- Helpers ----------
    def _populate_voices(self):
        if not self.engine: return
        names = [v.name for v in self.voices]
        self.voice_combo["values"] = names
        if names:
            self.voice_combo.current(0)

    def _update_mic_button_state(self):
        if sr is None or not pyaudio_ok:
            self.mic_btn.config(state="disabled")
        else:
            self.mic_btn.config(state="normal")


# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
