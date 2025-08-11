# Chat-app
Python LAN Chat Application implementation with socket programming and multithreading

#How to Run
Install dependencies:

bash
pip install rsa

On Peer 1 (Host):
chat = LANChat(host='0.0.0.0', port=5000)

On Peer 2 (Client):
chat = LANChat(host='<Peer1_IP>', port=5000)
