
import mimetypes
import socket, os
import protocol as prot

HOST = 'localhost'
PORT = 8000
ADDR = (HOST, PORT)
BUF_SIZE = 2048



if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5) #how much requests can i take

    print(f'Server connected on {ADDR}...')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Serving client connection from {addr}')
        prot.parseAndRespond(socket=client_socket)
