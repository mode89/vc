from xmlrpclib import ServerProxy

ADDRESS = "localhost", 1234

class Client(ServerProxy):

    def __init__(self):
        ServerProxy.__init__(
            self, "http://{0}:{1}".format(ADDRESS[0], ADDRESS[1]))
