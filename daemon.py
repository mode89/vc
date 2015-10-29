import esn
import input
import server

INPUT_COUNT = 13
NEURON_COUNT = 100
CONNECTIVITY = 0.5

class Daemon:

    def __init__(self):
        print("Generating network...")
        self.network = esn.create_network(
            inputCount=INPUT_COUNT,
            neuronCount=NEURON_COUNT,
            outputCount=1,
            connectivity=CONNECTIVITY,
            useOrthonormalMatrix=True)
        self.input_audio = input.Audio()
        self.server = server.Server()
        self.server.start()

    def loop(self):
        while True:
            self.network.set_inputs(self.input_audio.read())
        self.input.close()