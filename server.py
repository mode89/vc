from SimpleXMLRPCServer import SimpleXMLRPCServer
from SocketServer import ThreadingMixIn
from threading import Thread

ADDRESS = "127.0.0.1", 1234

class Server(ThreadingMixIn, SimpleXMLRPCServer):

    def __init__(self, daemon):
        SimpleXMLRPCServer.__init__(self, ADDRESS, allow_none=True)
        self.thread = Thread(target=self.serve_forever)
        self.thread.daemon = True
        self.register_instance(daemon)

    def start(self):
        self.thread.start()

    def shutdown(self):
        SimpleXMLRPCServer.shutdown(self)
        SimpleXMLRPCServer.server_close(self)
