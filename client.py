import tkinter as tk
from PIL import Image, ImageTk
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
    root.attributes('-fullscreen', True)  # Make UI full screen
    root.title("Doorbell")

    # Load doorbell image
    doorbell_img = Image.open("doorbell_icon.png")
    doorbell_img = doorbell_img.resize((200, 200), Image.ANTIALIAS)  # Resize image
    doorbell_icon = ImageTk.PhotoImage(doorbell_img)

    doorbell_button = tk.Button(root, image=doorbell_icon, command=doorbell_pressed)
    doorbell_button.pack(pady=20, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
