#!/usr/bin/python
import socket
import random

class webApp:

    def parse(self, request):
        metodo = request.split(' ',1)[0]
        recurso = request.split(' ',2)[1]
        parts = request.split('\r\n\r\n',1)
        if len (parts) == 2:
            cuerpo = parts[1]
        else:
            cuerpo = ""
        
        print 'metodo: '
        print metodo
        print 'recurso: '
        print recurso
        print 'cuerpo: '
        print cuerpo
        return (metodo, recurso, cuerpo)

    def process(self, parsedRequest):
        return ("200 OK", "<html><body><h1>Dummy</h1></body></html>")

    def __init__(self, hostname, port):

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)
        try:
            while True:
                print ('Waiting for connections')
                (recvSocket, address) = mySocket.accept()
                print ('HTTP request received (going to parse and process):')
                request = recvSocket.recv(2048)
                print (request)
                parsedRequest = self.parse(request)
                (returnCode, htmlAnswer) = self.process(parsedRequest)
                print ('Answering back...')
                recvSocket.send("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n")
                recvSocket.close()
        except KeyboardInterrupt:
            mySocket.close()
            print("\nExiting Ok")
