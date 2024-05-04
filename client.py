import tkinter as tk
from PIL import Image, ImageTk
import socket
import pyaudio
import wave

def doorbell_pressed():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    # Set up socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.7', 5678))  # Replace with Home PC's IP address

    # Send doorbell press signal to Home PC
    client_socket.send("doorbell_pressed".encode())

    # Record audio
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
    client_socket.sendall(audio_bytes)

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

    doorbell_button = tk.Button(root, image=doorbell_icon, command=doorbell_pressed)
    doorbell_button.pack(pady=20, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
