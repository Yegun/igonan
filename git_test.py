from socket import *
import sys
import threading

serverSocket = socket(AF_INET, SOCK_STREAM)
# Presuming the port number you provided (5679) is the one intended for use
serverPort = 5678
serverSocket.bind(("", serverPort))
serverSocket.listen()

def handle_client(connectionSocket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        message = connectionSocket.recv(1024)
        if not message:
            return  # Client has closed the connection

        filename = message.split()[1]
        print('File', filename, 'has been sent on', str(threading.current_thread().name))

        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # The connection should be closed after sending the data to the client
        connectionSocket.close()

def startprogram():
    serverSocket.listen()
    while True:
        # Accept a new connection
        connectionSocket, addr = serverSocket.accept()
        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        thread.start()

# This will start the server
print('Ready to serve...')
startprogram()
serverSocket.close()
sys.exit()