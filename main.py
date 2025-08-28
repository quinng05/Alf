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

listener.start()

print("Hold SPACEBAR to record. Press ESC to exit.")

try:
    listener.join()
except KeyboardInterrupt:
    print("\nExiting...")
    listener.stop()



