import socket
import os.path
import mimetypes
import hashlib
import time
import functions
#import tqdm

PORT = 8000
BUF_SIZE = 2048
#allowing multiple names for one resource the key is the previous and the value is the new name
redirect_dict = {'index112.html': 'index1212.html'}
#marks:
#only / is index.html
#it is not necessary to specify host
#it is not necessary to specify accept
#200 ok - it's ok
#301 moved permanently - moved location of file
#302 found - found file
#304 not modified
#404 not found
#cache is local memory that is taken from microprocessors -מטמון
#
def parseAndRespond(**kwargs):
    client_socket = kwargs.get('socket')
    headers = parse_http_request(client_socket)

    pieces = headers["first"].split("\r\n")
    #print(pieces[0])
    resource = headers["first"].split()[1][1:] #Getting the file to POST.

    if resource == '': #If no file was specified, then it is automatically the index.html.
        resource = 'index.html'
    if '?' in resource:
        command = resource.split('?')[0]
        command = command.replace('-','_')
        file_size = 0
        if command == "upload":
            file_size = headers["Content-Length"]
        parameters = resource.split('?')[1]
        transfer_file = getattr(functions, command)(parameters = parameters,socket= client_socket, size = file_size)
        resource = transfer_file
    etag = "None"
    last_modified = 'None1'
    if os.path.exists(resource):
        last_modified = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        etag = generate_etag_md5(resource)

    if resource in redirect_dict.keys():
        response = "HTTP/1.1 302 Found\r\n".encode()
        response += f"Location: {redirect_dict[resource]}\r\n".encode()
        response += "Connection: close\r\n".encode()
        response += "\r\n".encode()
        print(f"{pieces[0]} --> HTTP/1.1 302 Found")
        resource = None

    elif etag == headers.get('If-None-Match') and last_modified == headers.get("If-Modified-Since"):
        response = "HTTP/1.1 304 Not-Modified\r\n".encode()
        response += f"ETag: {etag}\r\n".encode()
        response += f"Last-Modified: {last_modified}\r\n".encode()
        response += "\r\n".encode()
        resource = None
        print(f"{pieces[0]} -> Response code: 304 Not Modified")

    elif os.path.exists(resource): #If it is found somewhere then we get the file specified.
        with open(resource, 'rb') as f:
            resource_data = f.read()
            response = 'HTTP/1.1 200 OK\r\n'.encode() #HEADER
            print(pieces[0] + ' --> HTTP/1.1 200 OK')
            #response += f'Content-Length: {resource_len}\r\n'.encode()
            #response += '\r\n'.encode()

    else: #No file was found - error 404 getting resource.
        resource = "404error.html"
        with open(resource, 'rb') as f:
            resource_data = f.read()
            response = 'HTTP/1.1 404 Not Found\r\n'.encode() #HEADER
            print(pieces[0] + ' --> HTTP/1.1 404 Not found')

    if resource is not None:
        resource_len = os.path.getsize(resource)
        content_type , _ = mimetypes.guess_type(resource) #type of send
        response += f"Host: localhost:{PORT}\r\n".encode()
        response += f'Content-Type: {content_type or "application/octet-stream"}\r\n'.encode()
        response += f'Content-Length: {resource_len}\r\n'.encode()
        response += f'Cache-Control: no cache, public\r\n'.encode()
        response += f'ETag: {etag}\r\n'.encode()
        response += f"Last-Modified: {last_modified}\r\n".encode()
        response += '\r\n'.encode() #seperating header and body

        response += resource_data #data size
    client_socket.sendall(response) #Sending the file.
    client_socket.close()

def generate_etag_md5(file_name):
    md5_hash =  hashlib.md5()
    try:
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(BUF_SIZE),b""):
                    md5_hash.update(chunk)
    except FileNotFoundError:
        return None

    return md5_hash.hexdigest()
def parse_http_request(client_socket)     :
    headers = {}
    request_data = ''
    while '\r\n\r\n' not in request_data:
        request_data += client_socket.recv(BUF_SIZE).decode('utf-8')

    headers_raw, body = request_data.split("\r\n\r\n")

    for line in headers_raw.split("\r\n"):
        if ': ' in line:
            header, data = line.split(": ")
            headers[header] = data
        else:
            headers["first"] = line



    return headers





