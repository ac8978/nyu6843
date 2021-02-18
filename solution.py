#import socket module
from socket import *
import sys

def webServer(port=13331):

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', port))
    serverSocket.listen(5)

    while True:
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:], "r")
            outputdata = f.read()
            #connectionSocket.send('\n') #blank line - necessary
            #connectionSocket.send('HTTP/1.1 200 OK\n')
            #connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n')
            #connectionSocket.send('Connection: close\n')
            #connectionSocket.send('Content-Length: 120\n')
            #connectionSocket.send('Content-Type: text/html\n')
            connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send('\r\n\r\n'.encode())
            connectionSocket.close()

        except IOError:
            connectionSocket.send('HTTP/1.1 404 File Not Found\r\n\r\n'.encode())
            connectionSocket.send('404 File Not Found'.encode())
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
   webServer(13331)
