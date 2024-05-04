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

    # Show recording status
    status_label.config(text="Recording in progress...", fg="blue")

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

    # Reset recording status
    status_label.config(text="Press doorbell to record", fg="black")

def send_audio(audio_data):
    # Set up socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.7', 5678))  # Update server IP address here

    # Send audio data to server
    client_socket.sendall(audio_data)

    # Close client socket
    client_socket.close()

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make UI full screen
    root.title("Doorbell UI")

    # Load doorbell image
    doorbell_img = Image.open("doorbell_icon.png")
    doorbell_img = doorbell_img.resize((200, 200), Image.ANTIALIAS)  # Resize image
    doorbell_icon = ImageTk.PhotoImage(doorbell_img)

    doorbell_button = tk.Button(root, image=doorbell_icon, command=start_recording)
    doorbell_button.pack(pady=20, fill=tk.BOTH, expand=True)

    # Recording status label
    global status_label
    status_label = tk.Label(root, text="Press doorbell to record", fg="black")
    status_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
