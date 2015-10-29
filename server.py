from SocketServer import BaseRequestHandler
from SocketServer import TCPServer
from SocketServer import ThreadingMixIn
from threading import Thread

ADDRESS = "localhost", 1234

class Server(ThreadingMixIn, TCPServer):

    def __init__(self, daemon):
        TCPServer.__init__(self, ADDRESS, Server.RequestHandler)
        self.thread = Thread(target=self.serve_forever)
        self.thread.daemon = True
        self.daemon = daemon

    def start(self):
        self.thread.start()

    def shutdown(self):
        TCPServer.shutdown(self)
        TCPServer.server_close(self)

    class RequestHandler(BaseRequestHandler):

        def handle(self):
            data = self.request.recv(1024)
            args = data.split()
            command = args[0]
            options = args[1:]
            getattr(self.server.daemon, command)(options)
