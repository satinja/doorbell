import socket

# Set up socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.7', 12345))  # Replace with Home PC's IP address

# Send doorbell press signal to Home PC
client_socket.send("doorbell_pressed".encode())

# Close client socket
client_socket.close()
