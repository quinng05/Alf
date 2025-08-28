import sys, os, subprocess, time, threading, queue, numpy as np
import sounddevice as sd
import webrtcvad
from pynput import keyboard
from model import set_model 



# ---- Set FasterWhisper model ----
this_model = set_model()
print("Current FW Model: ", this_model)



# ---- Audio streaming config ----
SR = 16000      # 16 kHz sample rate
FRAME_MS = 20   # 20 ms audio frames
FRAME_SAMPLES = SR * FRAME_MS // 1000       # Number of samples in each frame 
WINDOW_SEC = 1.0     # Streaming buffer window
TICK = 0.25     # Transcription call tick speed



# ---- State ----
recording = False   # Audio recording bool
q = queue.Queue()   # Audio queue 
stop_flag = False   # Transcription thread bool
last_print = ""     # Last transcript string shown in console
buf = b""           # Rolling buffer of raw PCM bytes to fill window on each tick
max_bytes = int(SR * WINDOW_SEC) * 2        # Max bytes allotted to buf (PCM = 2 bytes per sample)
last_tick = 0.0     # Tracks last Whisper call (last tick)



# ---- Capture & Conversion helpers ----
# int 16 PCM --> float32 in [-1, 1]
def pcm_to_f32(pcm: bytes):
    return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0  # converts PCM 16b value to normalized 32b float

# Audio callback joiner func
def audio_cb(indata, frames, time_info, status):
    # enqueue 20ms audio frames to stream while recording
    if recording:
        q.put(indata.copy())



# ---- Audio Streaming Recorder ----
def asr_worker():
    global buf, last_tick, last_print, stop_flag
    while not stop_flag:
        try:
            chunk = q.get(timeout=0.1)
        except queue.Empty:
            continue

        # rolling WINDOW_SEC buffer
        pcm = chunk.tobytes()
        buf += pcm
        if len(buf) > max_bytes:
            buf = buf[-max_bytes:]

        # throttle calls
        now = time.time()
        if now - last_tick < TICK:
            continue
        last_tick = now

        # require a little audio (~100 ms) before calling
        if len(buf) < FRAME_SAMPLES * 2 * 5:
            continue

        audio = pcm_to_f32(buf)
        segments, _ = this_model.transcribe(
            audio,
            language="en",
            beam_size=1, best_of=1, temperature=0
        )
        text = "".join(s.text for s in segments).strip()
        if text:
            # single-line interim update
            sys.stdout.write("\r" + text + " " * 8)
            sys.stdout.flush()
            last_print = text



# ---- Keyboard input control ----
def start_recording():
    global recording
    if not recording:
        recording = True
        print("🔴 Recording started...")

def stop_recording():
    global recording
    if recording:
        recording = False
        print("⚫ Recording stopped")

def on_press(key):
    if key == keyboard.Key.space:
        start_recording()

def on_release(key):
    if key == keyboard.Key.space:
        stop_recording()
    elif key == keyboard.Key.esc:
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True  
)

# Start listening for keyboard input
listener.start()

# start ASR worker thread
th = threading.Thread(target=asr_worker, daemon=True)
th.start()

print("Hold SPACEBAR to record. Press ESC to exit.")

# open mic: 16 kHz mono, 20 ms frames
with sd.InputStream(samplerate=SR, channels=1, dtype='int16',
                    blocksize=FRAME_SAMPLES, callback=audio_cb, latency='low'):
    try:
        listener.join()
    except KeyboardInterrupt:
        print("\nExiting...")
        listener.stop()

# clean shutdown
stop_flag = True
th.join(timeout=1.0)


