import socket

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, _ = server_socket.accept() # wait for client
    data = client.recv(1024).decode()
    
    if data.split(" ")[1] == "/":
        client.send(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
