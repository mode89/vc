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
        self.server = server.Server(self)
        self.server.start()
        self.state = Daemon.RunningState()

    def loop(self):
        self.working = True
        while self.working:
            self.state.step(self)
        self.input_audio.close()

    def exit(self):
        print("Exiting...")
        self.working = False

    def train(self, command):
        self.state.train(self, command)

    def train_ambient(self, command):
        self.state.train_ambient(self, command)

    class State:

        def step(self, daemon):
            raise NotImplementedError()

        def train(self, daemon, command):
            if command == "start":
                self.train_start(daemon)
            elif command == "stop":
                self.train_stop(daemon)
            else:
                raise RuntimeError(
                    "Unknown command: {0}".format(command))

        def train_start(self, daemon):
            raise NotImplementedError()

        def train_stop(self, daemon):
            raise NotImplementedError()

        def train_ambient(self, daemon, command):
            if command == "start":
                self.train_ambient_start(daemon)
            elif command == "stop":
                self.train_ambient_stop(daemon)
            else:
                raise RuntimeError(
                    "Unknown command: {0}".format(command))

        def train_ambient_start(self, daemon):
            raise NotImplementedError()

        def train_ambient_stop(self, daemon):
            raise NotImplementedError()

    class RunningState(State):

        def step(self, daemon):
            daemon.network.set_inputs(daemon.input_audio.read())

        def train_start(self, daemon):
            print("Start training...")
            daemon.state = Daemon.TrainingState()

        def train_stop(self, daemon):
            raise Warning("Training hasn't been started.")

        def train_ambient_start(self, daemon):
            print("Start ambient training...")
            daemon.state = Daemon.AmbientTrainingState()

        def train_ambient_stop(self, daemon):
            raise Warning("Ambient training hasn't been started.")

    class TrainingState(State):

        def step(self, daemon):
            daemon.network.set_inputs(daemon.input_audio.read())

        def train_start(self, daemon):
            raise Warning("Training has already been started.")

        def train_stop(self, daemon):
            print("Stop training...")
            daemon.state = Daemon.RunningState()

        def train_ambient_start(self, daemon):
            raise Warning("Cannot start ambient training while training.")

        def train_ambient_stop(self, daemon):
            raise Warning("Ambient training hasn't been started.")

    class AmbientTrainingState(State):

        def step(self, daemon):
            daemon.network.set_inputs(daemon.input_audio.read())
            daemon.network.train_online([0.0])
