#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import webAPP
import pickle

# -------------- Port Set Up --------------
G_host = socket.gethostname()
G_port = 1234


# -------------- Functions --------------
def initFile(name):
    try:
        File = open(name, 'r')
        File.close
    except:
        File = open(name, 'wb')
        File.close

def SaveURLs(Dic, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(Dic, f, pickle.HIGHEST_PROTOCOL)

def LoadURLs(name ):
    try:
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return {}

def decorateHTML (text):
    return ("<html><body>" + text + "</body></html>")

def myURL ():
    return 'http://'+str(G_host)+':'+str(G_port)


# -------------- Classes --------------
class acortaURL (webAPP.webApp):
    """ -----------  Clave  Valor  -----------"""
    # Creates file "URLs.pkl" for further use, if doesn't exists 
    urlsLargas = 'URLsLong'
    urlsCortas = 'URLsShort'
    initFile((urlsLargas+'.pkl'))
    initFile((urlsCortas+'.pkl'))
    urlLargas = {} # URL   SeqN
    urlCortas = {} # SeqN  URL
    urlLargas = LoadURLs(urlsLargas)
    urlCortas = LoadURLs(urlsCortas)
    seqNumb = len(urlLargas)

    def process(self, parsedRequest):
        metodo, recurso, cuerpo = parsedRequest # Get /... <html>...
        
        if metodo == 'GET':
            # Recibido GET/
            if recurso == '/':
                httpCode = '200 OK'
                htmlBody =   '<html><body>'\
                            +'<form method="POST" action="">'\
                            +'URL: <input type="text" name="url"><br>'\
                            +'<input type="submit" value="Enviar">'\
                            +'</form>'\
                            +'<p1>En Cache: '+str(self.urlLargas)+'</p1>'\
                            +'</body><title>Acortador</title>'\
                            +'</html>'
            # Recibido GET/favicon.ico
            elif recurso == '/favicon.ico':
                print 'Recibida peticion "favicon"'
                httpCode = '200 OK'
                htmlBody=''
            # Recibido GET/recurso(n)
            else:
                urlCorta = myURL()+'/'+str(int(recurso[1:]))
                try:
                    urlDestino = self.urlCortas[urlCorta]
                    httpCode = '303 See Other\r\nLocation: ' + urlDestino
                    htmlBody = ''
                except KeyError:
                    print 'Detectada peticion inconsistente'
                    httpCode = '404 Not Found'
                    htmlBody = decorateHTML('<h3>Recurso no disponible</h3>'\
                                            +'<p>Codigo de error: 404</p>')
        # Recibido POST/
        elif metodo == 'POST' or metodo == 'PUT':
            cuerpo=cuerpo.replace('%3A',':') # Recibo estos strings...
            cuerpo=cuerpo.replace('%2F','/')
            if cuerpo[0:4] == 'url=': # POST de formulario o poster con "url..."
                cuerpo = cuerpo[4:] # Quito el url=
            if cuerpo[0:7] != 'http://': # http:// en caso de no haberlo
                cuerpo = 'http://' + cuerpo
                
                
            if cuerpo in self.urlCortas:
                urllarga = self.urlCortas[cuerpo]
                urlCorta = cuerpo
                cuerpo = urllarga
                httpCode = '200 OK' # Redirección temporizada
                htmlBody = decorateHTML('<title>URL Acortada</title>'\
                                        +'<h3>URL corta ya incluida:</h3>'\
                                        +'<p1>URL Larga: <a href= '\
                                        +cuerpo + '>' + cuerpo + '</a></p>'\
                                        +'<p>URL Corta: <a href= '\
                                        +urlCorta + '>'\
                                        +urlCorta + '</a></p>')
            else:
                try: # Entrego la url corta al navegador
                    urlCorta = self.urlLargas[cuerpo]
                    print 'URL encontrada, devolviendo almacenada'
                except KeyError:
                    print 'URL no encontrada, creando...'
                    urlCorta = myURL()+'/'+str(self.seqNumb)
                    self.urlLargas[cuerpo] = urlCorta # Larga, Corta
                    self.urlCortas[urlCorta] = cuerpo
                    # Almacenamiento en ficheros:
                    SaveURLs(self.urlLargas, self.urlsLargas)
                    SaveURLs(self.urlCortas, self.urlsCortas)
                    self.seqNumb = self.seqNumb + 1
                httpCode = '200 OK' # Redirección temporizada
                htmlBody = decorateHTML('<title>URL Acortada</title>'\
                                        +'<p1>URL Larga: <a href= '\
                                        +cuerpo + '>' + cuerpo + '</a></p>'\
                                        +'<p>URL Corta: <a href= '\
                                        +urlCorta + '>'\
                                        +urlCorta + '</a></p>')
        else:
            print 'Error: Recibido metodo desconocido'

        return (httpCode,htmlBody)


if __name__ == "__main__":
    RunAPP = acortaURL(G_host, G_port)











