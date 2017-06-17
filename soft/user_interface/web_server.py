#!/usr/bin/python3
# -*- coding: latin-1 -*-
"""
@author: thibaud
"""
import http.server
import logging
import socketserver
import sys
from threading import Thread


# This class provide a thread for the audio module
class WebServerModule(Thread):
    def __init__(self):
        Thread.__init__(self)
        # Serveur http de base delivrant le contenu du repertoire courant via le port indique.
        self.handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", 80), self.handler)
        self.terminated = False  # Stop flag

    # Thread recording audio in
    def run(self):
        logging.info("Starting web server thread")
        # This loop condition have to be checked frequently, so the code inside may not be blocking
        while not self.terminated:
            self.httpd.serve_forever()

    # Method called to stop the thread
    def stop(self):
        logging.info('Stopping web server...')
        self.terminated = True
        self.httpd.shutdown()


# Main function used if the script is started alone
def main():
    server = WebServerModule()
    server.start()
    try:
        server.join()
    except KeyboardInterrupt:
        print('Execution interrupted by user, stopping...')
        server.stop()
        server.join()
        sys.exit(0)  # Finaly, exit


# If main program, start server
if __name__ == "__main__":
    main()
