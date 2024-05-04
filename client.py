import tkinter as tk
import socket

def doorbell_pressed():
    # Set up socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.7', 5678))  # Replace with Home PC's IP address

    # Send doorbell press signal to Home PC
    client_socket.send("doorbell_pressed".encode())

    # Close client socket
    client_socket.close()

def main():
    root = tk.Tk()
    root.title("Doorbell UI")

    doorbell_button = tk.Button(root, text="Press Doorbell", command=doorbell_pressed)
    doorbell_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
