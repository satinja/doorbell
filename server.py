import socket
import pyaudio
import wave
import threading

class DoorbellServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None
        self.bell_sound = wave.open("bell_sound.wav", 'rb')

    def start(self):
        self.server_socket.bind(('0.0.0.0', 5678))  # Change port number if needed
        self.server_socket.listen(1)
        print("Server is listening...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def play_bell_sound(self):
        # Set up audio stream
        if not self.audio_stream:
            self.audio_stream = self.audio.open(format=self.audio.get_format_from_width(self.bell_sound.getsampwidth()),
                                                channels=self.bell_sound.getnchannels(),
                                                rate=self.bell_sound.getframerate(),
                                                output=True)
        # Play bell sound
        print("Playing bell sound...")
        data = self.bell_sound.readframes(1024)
        while data:
            self.audio_stream.write(data)
            data = self.bell_sound.readframes(1024)

    def handle_client(self, client_socket):
        # Play bell sound when doorbell pressed
        self.play_bell_sound()

        # Receive and play audio data from client
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if not self.audio_stream:
                self.audio_stream = self.audio.open(format=pyaudio.paInt16,
                                                    channels=1,
                                                    rate=44100,
                                                    output=True)
            self.audio_stream.write(data)

        # Clean up
        client_socket.close()

def main():
    doorbell_server = DoorbellServer()
    doorbell_server.start()

if __name__ == "__main__":
    main()
