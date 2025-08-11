import socket
import threading
import rsa  # For encryption

class LANChat:
    def __init__(self, host='localhost', port=5000):
        # Generate RSA keys
        (self.pub_key, self.priv_key) = rsa.newkeys(512)
        
        # Socket setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        
        # Client variables
        self.connection = None
        self.peer_pub_key = None

    def start(self):
        print("LAN Chat started. Waiting for connections...")
        threading.Thread(target=self.accept_connections).start()
        threading.Thread(target=self.send_messages).start()

    def accept_connections(self):
        self.connection, addr = self.sock.accept()
        print(f"Connected to {addr}")
        
        # Key exchange
        self.connection.send(self.pub_key.save_pkcs1())
        self.peer_pub_key = rsa.PublicKey.load_pkcs1(self.connection.recv(1024))

    def send_messages(self):
        while True:
            message = input("You: ")
            encrypted = rsa.encrypt(message.encode(), self.peer_pub_key)
            self.connection.send(encrypted)

    def receive_messages(self):
        while True:
            if self.connection:
                encrypted = self.connection.recv(1024)
                message = rsa.decrypt(encrypted, self.priv_key).decode()
                print(f"\nFriend: {message}")

if __name__ == "__main__":
    chat = LANChat()
    threading.Thread(target=chat.receive_messages).start()
    chat.start()
