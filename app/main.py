import socket
from threading import Thread

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client, _ = server_socket.accept() # wait for client
        Thread(target=handle_client, args=[client]).start()

def handle_client(client: socket.socket):
    data = client.recv(4096).decode()
    if data.split(" ")[1] == "/":
        client.send(b"HTTP/1.1 200 OK\r\n\r\n")
   
    elif data.split(" ")[1].startswith("/echo/"):
        text = data.split(" ")[1].split("echo")[1].split("/")[1]
    
        client.send(b"HTTP/1.1 200 OK\r\n")
        client.send(b"Content-Type: text/plain\r\n")
        client.send(f"Content-Length: {len(text)}\r\n".encode("ascii"))
        client.send(b"\r\n")
        client.send(text.encode("ascii"))
        
    elif data.split(" ")[1].startswith("/user-agent"):
        text = data.split("\r\n")[2].split(" ")[1]
        client.send(b"HTTP/1.1 200 OK\r\n")
        client.send(b"Content-Type: text/plain\r\n")
        client.send(f"Content-Length: {len(text)}\r\n".encode("ascii"))
        client.send(b"\r\n")
        client.send(text.encode("ascii"))
        
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
if __name__ == "__main__":
    main()
