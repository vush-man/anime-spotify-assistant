# Anime Spotify Assistant 🎶👧

A fun desktop assistant with an **anime girl popup** that listens to your voice,  
finds songs on Spotify, speaks back to you, and plays them instantly.  

Built with **Tkinter**, **Whisper (OpenAI)** for speech recognition, and **Voicevox** for anime-style speech synthesis.  

---

## ✨ Features
- 🎤 **Voice recognition** with Whisper (accurate STT)
- 🎶 **Spotify Premium playback** using Spotipy
- 🖼 Animated GIF-based **anime girl UI**
- 🗣 **Voicevox** text-to-speech for responses
- ⌨️ Manual text entry fallback
- 🔄 Asynchronous design (UI never freezes during speech or playback)

---

## 📂 Project Structure
```
anime-spotify-assistant/
│── main.py              # Entry point
│── ui.py                # Tkinter UI + GIF handling
│── spotify_client.py    # Spotify API wrapper
│── voice.py             # Speech recognition + TTS (Whisper + Voicevox)
│── config.py            # Constants & environment setup
│── requirements.txt     # Python dependencies
│── env_example.txt      # env example file for Spotify credentials
│── assets/
│    ├── anime_idle.gif
│    ├── anime_sing.gif
│    └── anime_girl.png
```

---

## 🚀 Setup

### 1. Clone and Install Dependencies
```bash
git clone https://github.com/vush-man/anime-spotify-assistant.git
cd anime-spotify-assistant
pip install -r requirements.txt
```

### 2. Setup Spotify App
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)  
2. Create an app → copy **Client ID** and **Client Secret**  
3. Add Redirect URI:  
   ```
   http://localhost:8888/callback
   ```
   and save.

### 3. Configure Environment
Copy `env_example.txt` to `.env` and fill in your credentials:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

### 4. Assets
Place your anime assets inside `assets/`:
- `anime_idle.gif` → idle animation  
- `anime_sing.gif` → singing animation  
- `anime_girl.png` → fallback static image  

### 5. Voicevox Server
1. Make sure you have a **Voicevox Engine** running locally
2. Download the corresponding engine form [here](https://github.com/VOICEVOX/voicevox_engine/releases/tag/0.24.1)
3. Unzip it in a directory, then open terminal in that directory and
```bash
./run
```

---

## ▶ Usage
Start the assistant:
```bash
python main.py
```

- Click **🎤 Listen** and say a song name  
- Or type a song into the entry box and hit **▶ Play Typed**  
- The anime girl will respond and play your track on Spotify  

---

## 📝 Notes
- Spotify Premium account required  
- You must have Spotify open on **some device** (desktop, phone, or web player)  
- First run will open a browser for Spotify authorization (token cached in `.cache`)  
- Whisper model will download on first run (`small` by default)  

---

## 💡 Future Ideas

- Lip-sync animation tied to TTS playback  
- Support playlists and podcast playback  
- Integration with other music services  

---

## 📜 License
MIT License © 2025 vush-man
