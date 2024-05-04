import socket
import winsound  # For playing audio on Windows

# Set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Change port number if needed
server_socket.listen(1)

print("Server is listening...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    # Receive data from client
    data = client_socket.recv(1024).decode()
    if data == "doorbell_pressed":
        print("Doorbell pressed. Playing audio.")
        # Play audio
        winsound.PlaySound("bell_sound.wav", winsound.SND_FILENAME)
        client_socket.close()
        break

# Close server socket
server_socket.close()
