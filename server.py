import socket
import threading

HOST = '127.0.0.1'
PORT = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"Received encrypted message: {message}")
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()