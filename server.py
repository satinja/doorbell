import socket
import pyaudio
import threading
import wave

def handle_client(client_socket, audio_stream):
    while True:
        # Receive data from client
        data = client_socket.recv(1024)
        if not data:
            break

        # Play received audio data
        audio_stream.write(data)

    client_socket.close()

def main():
    # Set up socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5678))  # Change port number if needed
    server_socket.listen(1)

    print("Server is listening...")

    # Initialize PyAudio stream
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=44100,
                              output=True)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, audio_stream))
        client_thread.start()

    # Cleanup
    server_socket.close()
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()

if __name__ == "__main__":
    main()
