from config import VOICE_VOLUME
import threading, tempfile, requests, numpy as np, sounddevice as sd
import whisper, speech_recognition as sr

def speak(text: str, volume: float = VOICE_VOLUME):
    params = {"text": text, "speaker": 1}
    query = requests.post("http://localhost:50021/audio_query", params=params)
    synthesis = requests.post("http://localhost:50021/synthesis", params=params, data=query.content)
    audio = np.frombuffer(synthesis.content, dtype=np.int16).astype(np.float32)

    audio *= volume
    audio = np.clip(audio, -32768, 32767).astype(np.int16)

    sd.play(audio, samplerate=24000)
    sd.wait()

def speak_async(text: str, volume: float = VOICE_VOLUME, on_complete=None):
    def worker(on_complete=on_complete, volume=volume):
        speak(text, volume=volume)
        if on_complete:
            on_complete()
    threading.Thread(target=worker, daemon=True).start()

whisper_model = whisper.load_model("small")

def recognize_from_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source, timeout=8, phrase_time_limit=8)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        temp_filename = f.name

    result = whisper_model.transcribe(temp_filename)
    return result["text"].strip()
