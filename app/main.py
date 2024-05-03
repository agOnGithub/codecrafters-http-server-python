import socket
from threading import Thread
import sys
import os

def main():
    fdir = ""
    if len(sys.argv) == 3 and sys.argv[1] == "--directory":
        fdir = sys.argv[2]
        
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client, addr = server_socket.accept() # wait for client
        Thread(target=handle_client, args=(client, addr, fdir)).start()

def handle_client(client: socket.socket, addr, fdir):    
    data = client.recv(4096).decode()
    if data.split(" ")[1] == "/":
        client.send(b"HTTP/1.1 200 OK\r\n\r\n")
        
    elif data.split(" ")[1].startswith("/files/"):
        fname = data.split(" ")[1].split("/")[2]
        fpath = fdir + fname
        print(data.split(" ")[1])
        #if data.startswith("GET"):
        try:
            f = open(fpath, "rb")
            blob = f.read()
            f.close()
            response = bytearray(b"HTTP/1.1 200 OK\r\n")
            response.extend(b"Content-Type: application/octet-stream\r\n")
            response.extend(f"Content-Length: {len(blob)}\r\n\r\n".encode())
            response.extend(blob)
            client.send(response)
        except:
            client.send(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n") 
       # else:
           # file_contents = data.split("\r\n\r\n")[1].encode("ascii")
           # with open(fpath, "wb") as file:
           #     file.write(file_contents)
       #client.send(b"HTTP/1.1 201 Created\r\n")
   
    elif data.split(" ")[1].startswith("/echo/"):
        text = data.split(" ")[1].split("echo")[1].split("/")[1]
        response = bytearray("HTTP/1.1 200 OK\r\n".encode("ascii"))
        response.extend(b"Content-Type: text/plain\r\n")
        response.extend(f"Content-Length: {len(text)}\r\n\r\n".encode("ascii"))
        client.send(response)
        client.send(text.encode("ascii"))
        
    elif data.split(" ")[1].startswith("/user-agent"):
        text = data.split("\r\n")[2].split(" ")[1]
        response = bytearray("HTTP/1.1 200 OK\r\n".encode("ascii"))
        response.extend(b"Content-Type: text/plain\r\n")
        response.extend(f"Content-Length: {len(text)}\r\n\r\n".encode("ascii"))
        client.send(response)
        client.send(text.encode("ascii"))
        
    else:
        client.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
if __name__ == "__main__":
    main()
