import sys, os, subprocess, time, threading, queue, numpy as np
import sounddevice as sd
import webrtcvad
from pynput import keyboard
from model import set_model 

ppid = os.getppid()
parent = subprocess.check_output(["ps", "-o", "comm=", "-p", str(ppid)])
print("Parent process:", parent.decode().strip())
          
this_model = set_model()
print("Current FW Model: ", this_model)

recording = False

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



