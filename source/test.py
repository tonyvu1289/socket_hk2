import socket
import time
#get ip
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
#set up socket and listen
server = socket.socket()
server.bind((host,80))
print("ip : ",host)
server.listen(1)
#receive message from client
while True:
    #set up new socket (vanish after this loop)
    stream,addr=server.accept()
    #receive request from client by new socket
    try:
        request=stream.recv(10000)
    except socket.error as msg:
        print("oh shit")
    print(request)
    #process request
    request=request.decode()
    request_lines=request.splitlines()
    print(request) #debug
    
    if(len(request_lines)<=1):
        continue
    #method is word [0] at line [0] in request
    method = request_lines[0].split(' ')[0]
    
    if(method == "GET"):
        file_name=request_lines[0].split(' ')[1]
        file_name=file_name.split('/')[1]
        if(file_name==""):
            file_name="index.html"
        file=open(file_name,"rb")
        response_data=file.read()
        response_head="HTTP/1.1 200 OK\n"
    elif(method == "POST"):
        header = '''HTTP/1.1 301 Moved Permanently\nLocation:/post.html'''
        stream.send(header.encode())
        stream.close()
        continue
    if(file_name.endswith(".html")):
        response_head+="Content-Type: text/html\n\n"
    elif(file_name.endswith(".png")):
        response_head+="Content-Type: image/png\n\n"
    response = response_head.encode()+response_data
    print(response)
    stream.send(response)
    stream.close()
