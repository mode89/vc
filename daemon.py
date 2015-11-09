from Queue import Queue
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
        self.output_queue = None

    def loop(self):
        self.working = True
        while self.working:
            self.state.step(self)
            if self.output_queue is not None:
                output = self.network.capture_output(1)
                self.output_queue.put(output)
        self.input_audio.close()

    def exit(self):
        print("Exiting...")
        self.working = False

    def calibrate(self, command):
        self.state.calibrate(self, command)

    def train(self, command):
        self.state.train(self, command)

    def train_ambient(self, command):
        self.state.train_ambient(self, command)

    def enable_output_capturing(self, enable):
        if enable:
            self.output_queue = Queue()
        else:
            self.output_queue = None

    def fetch_output(self):
        outputs = []
        size = self.output_queue.qsize()
        for i in range(size):
            value = self.output_queue.get()
            outputs.append(value)
        return outputs

    class State:

        def step(self, daemon):
            raise NotImplementedError()

        def calibrate(self, daemon, command):
            if command == "start":
                self.calibrate_start(daemon)
            elif command == "stop":
                self.calibrate_stop(daemon)
            else:
                raise RuntimeError(
                    "Unknown command: {0}".format(command))

        def calibrate_start(self, daemon):
            raise NotImplementedError()

        def calibrate_stop(self, daemon):
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

        def calibrate_start(self, daemon):
            print("Start calibration...")
            daemon.state = Daemon.CalibrationState()

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

    class CalibrationState(State):

        def step(self, daemon):
            pass

        def calibrate_stop(self, daemon):
            print("Stop calibration...")
            daemon.state = Daemon.RunningState()

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
