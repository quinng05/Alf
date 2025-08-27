import os
from pynput import keyboard
import time
from model import set_model 

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

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print("Hold SPACEBAR to record. Press ESC to exit.")

try:
    listener.join()
except KeyboardInterrupt:
    print("\nExiting...")
    listener.stop()



