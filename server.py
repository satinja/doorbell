import socket
import pyaudio

def play_audio(data):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
    stream.write(data)
    stream.close()
    audio.terminate()

def main():
    # Set up socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5678))  # Change port number if needed
    server_socket.listen(1)

    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")

        # Receive data from client
        data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            data += chunk

        if data:
            print("Received audio data.")
            play_audio(data)

        client_socket.close()

    # Close server socket
    server_socket.close()

if __name__ == "__main__":
    main()
