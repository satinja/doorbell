import tkinter as tk
from PIL import Image, ImageTk
import socket
import pyaudio
import wave
import threading
import time

def start_recording():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    # Show recording progress bar
    progress_bar.start()

    # Start recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    print("Recording...")
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop recording and close stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert audio frames to bytes and send to server
    audio_bytes = b''.join(frames)
    send_audio(audio_bytes)

    # Hide progress bar
    progress_bar.stop()

def send_audio(audio_data):
    # Set up socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.7', 5678))  # Update server IP address here

    # Send audio data to server
    client_socket.sendall(audio_data)

    # Close client socket
    client_socket.close()

def main():
    global progress_bar

    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make UI full screen
    root.title("Doorbell UI")

    # Load doorbell image
    doorbell_img = Image.open("doorbell_icon.png")
    doorbell_img = doorbell_img.resize((200, 200), Image.ANTIALIAS)  # Resize image
    doorbell_icon = ImageTk.PhotoImage(doorbell_img)

    doorbell_button = tk.Button(root, image=doorbell_icon, command=start_recording)
    doorbell_button.pack(pady=20, fill=tk.BOTH, expand=True)

    # Progress bar
    progress_bar = tk.ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
