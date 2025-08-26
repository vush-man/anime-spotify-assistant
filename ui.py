import os, threading, queue, tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from spotify_client import SpotifyClient
from voice import speak_async, speak, recognize_from_mic
from config import APP_TITLE

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100):
        super().__init__(master, bg="#0b0f19")
        self.delay = delay
        self.frames = []
        self.idx = 0
        self.anim_id = None
        self.load_gif(path)

    def load_gif(self, path):
        if self.anim_id:
            self.after_cancel(self.anim_id)
            
        try:
            im = Image.open(path)
            frames = []
            while True:
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(len(frames))
        except EOFError:
            pass

        self.frames = frames
        self.idx = 0
        if self.frames:
            self.configure(image=self.frames[0])
            self.after(self.delay, self.play)

    def play(self):
        if self.frames:
            self.idx = (self.idx + 1) % len(self.frames)
            self.configure(image=self.frames[self.idx])
            self.anim_id = self.after(self.delay, self.play)

class AnimeSpotifyUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("500x500")
        self.root.resizable(True, True)

        self.root.after(50, lambda: speak_async("おかえりなさい、ダーリン"))

        self.frame = tk.Frame(self.root, bg="#0b0f19")
        self.frame.pack(fill=tk.BOTH, expand=True)

        if os.path.exists("assets/anime_idle.gif"):
            self.image_label = AnimatedGIF(self.frame, "assets/anime_idle.gif", delay=80)
        else:
            self.image_label = tk.Label(self.frame, bg="#0b0f19", text="[Missing anime.gif]", fg="red")
        self.image_label.pack(pady=16)

        self.status_var = tk.StringVar(value="Hi! Click 'Listen' and say a song.")
        self.status = tk.Label(self.frame, textvariable=self.status_var,
                               fg="#d1e7ff", bg="#0b0f19", wraplength=360, justify="center")
        self.status.pack(pady=6)

        self.entry = tk.Entry(self.frame, width=36)
        self.entry.pack(pady=8)
        self.entry.insert(0, "Or type a song here…")
        self.entry.bind("<FocusIn>", lambda e: self.entry.delete(0, tk.END))

        btn_frame = tk.Frame(self.frame, bg="#070b14")
        btn_frame.pack(pady=12)

        self.listen_btn = tk.Button(btn_frame, text="🎤 Listen", width=12, command=self.on_listen)
        self.listen_btn.grid(row=0, column=0, padx=6)

        self.play_btn = tk.Button(btn_frame, text="▶ Play Typed", width=12, command=self.on_play_typed)
        self.play_btn.grid(row=0, column=1, padx=6)

        self.sp_client = None

        self.q = queue.Queue()
        self.root.after(100, self._poll_queue)

    def say_and_status(self, text: str):
        self.status_var.set(text)
        speak_async(text)

    def lazy_spotify(self):
        if self.sp_client is None:
            self.status_var.set("Connecting to Spotify... (authorize in browser if prompted)")
            self.sp_client = SpotifyClient()
            self.status_var.set("Connected. Say a song!")
        return self.sp_client

    def on_listen(self):
        self.listen_btn.config(state=tk.DISABLED)
        self.status_var.set("Listening... Say the song name.")

        if os.path.exists("assets/anime_idle.gif"):
            self.image_label.load_gif("assets/anime_idle.gif")

        speak_async("Listening... Say the song name.", on_complete=lambda:
        threading.Thread(target=self._listen_worker, daemon=True).start())

    def on_play_typed(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showinfo(APP_TITLE, "Type a song first.")
            return
        self._dispatch_play(query)

    def _listen_worker(self):
        try:
            text = recognize_from_mic()
            if not text:
                self.q.put(("error", "I didn't catch anything. Please try again."))
                return
            self.q.put(("heard", text))
        except Exception as e:
            self.q.put(("error", str(e)))

    def _dispatch_play(self, query: str):
        self.status_var.set(f"Searching: {query}")
        threading.Thread(target=self._play_worker, args=(query,), daemon=True).start()

    def _play_worker(self, query: str):
        try:
            sp = self.lazy_spotify()
            uri, label = sp.search_track_uri(query)
            if not uri:
                self.q.put(("error", f"Couldn't find: {query}"))
                return
            
            speak_async(f"Playing {label} on Spotify")
            sp.play_track(uri)

            if os.path.exists("assets/anime_sing.gif"):
                self.q.put(("gif", "assets/anime_sing.gif"))

            self.q.put(("status", f"Now Playing: {label}"))

        except Exception as e:
            self.q.put(("error", str(e)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.q.get_nowait()
                if kind == "heard":
                    self.status_var.set(f"You said: {payload}")
                    self._dispatch_play(payload)
                elif kind == "say":
                    self.say_and_status(payload)
                elif kind == "status":
                    self.status_var.set(payload)
                elif kind == "gif":
                    self.image_label.load_gif(payload)
                elif kind == "error":
                    self.status_var.set(payload)
                    messagebox.showerror(APP_TITLE, payload)

                self.listen_btn.config(state=tk.NORMAL)

        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)