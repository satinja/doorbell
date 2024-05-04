import tkinter as tk
from PIL import Image, ImageTk
import socket
import pyaudio
import threading
import wave

class DoorbellClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def connect_to_server(self):
        self.client_socket.connect(self.server_address)

    def start_recording(self):
        self.client_socket.sendall(b'Doorbell pressed')  # Send signal to server
        frames = []
        print("Recording...")
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                      input=True, frames_per_buffer=self.CHUNK)
        for _ in range(0, int(self.RATE / self.CHUNK * 5)):  # Record for 5 seconds
            data = self.stream.read(self.CHUNK)
            frames.append(data)
        print("Finished recording.")

        # Convert audio frames to bytes and send to server
        audio_bytes = b''.join(frames)
        self.send_audio(audio_bytes)

    def send_audio(self, audio_data):
        self.client_socket.sendall(audio_data)

    def close(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        self.client_socket.close()

class DoorbellApp:
    def __init__(self, root, client):
        self.root = root
        self.client = client

        # Load doorbell image
        doorbell_img = Image.open("doorbell_icon.png")
        doorbell_img = doorbell_img.resize((200, 200), Image.ANTIALIAS)  # Resize image
        self.doorbell_icon = ImageTk.PhotoImage(doorbell_img)

        # Doorbell button
        self.doorbell_button = tk.Button(root, image=self.doorbell_icon, command=self.doorbell_pressed)
        self.doorbell_button.pack(pady=20, fill=tk.BOTH, expand=True)

    def doorbell_pressed(self):
        # Start recording when doorbell pressed
        threading.Thread(target=self.client.start_recording).start()

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make UI full screen
    root.title("Doorbell UI")

    server_address = ('192.168.1.7', 5678)  # Update server IP address here
    doorbell_client = DoorbellClient(server_address)
    doorbell_client.connect_to_server()

    app = DoorbellApp(root, doorbell_client)
    root.mainloop()

    doorbell_client.close()

if __name__ == "__main__":
    main()
