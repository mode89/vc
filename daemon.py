from Queue import Queue
import esn
import input
import mfcc
import numpy
import server
import struct
import time
import wave

INPUT_COUNT = 13
NEURON_COUNT = 500
CONNECTIVITY = 0.5
TIME_STEP = 0.01
PULSE_MAGNITUDE = 0.7
PULSE_WIDTH = 0.15

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
        print("Free running...")
        self.state = Daemon.RunningState()
        self.output_queue = None
        self.input_frames = None

    def loop(self):
        self.working = True
        while self.working:
            frames = self.input_audio.read()
            if self.input_frames is not None:
                self.input_frames = numpy.append(self.input_frames, frames)
            mfcc_features = mfcc.mfcc(frames)
            self.state.step(self, mfcc_features)
            if self.output_queue is not None:
                output = self.network.capture_output(1)
                self.output_queue.put(output)
        self.input_audio.close()

    def exit(self):
        print("Exiting...")
        self.working = False

    def calibrate(self, command):
        self.state.calibrate(self, command)

    def capture_input(self, command):
        if command == "start":
            print("Start input capturing...")
            self.input_frames = numpy.array([])
        elif command == "stop":
            print("Stop input capturing...")
            wave_file = wave.open("input.wav", "wb")
            wave_file.setnchannels(1)
            wave_file.setsampwidth(2)
            wave_file.setframerate(44100)
            input_frames = self.input_frames * (2 ** 15)
            wave_file.writeframes(
                struct.pack(
                    "{0}h".format(len(input_frames)), *input_frames))
            wave_file.close()
            self.input_frames = None
        else:
            raise RuntimeError(
                "Undefined command: {0}".format(command))

    def train(self, command, period):
        self.state.train(self, command, period)

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

        def step(self, daemon, mfcc_features):
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

        def train(self, daemon, command, period):
            if command == "start":
                self.train_start(daemon, period)
            elif command == "stop":
                self.train_stop(daemon)
            else:
                raise RuntimeError(
                    "Unknown command: {0}".format(command))

        def train_start(self, daemon, period):
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

        def step(self, daemon, mfcc_features):
            daemon.network.set_inputs(mfcc_features)
            daemon.network.step(TIME_STEP)

        def calibrate_start(self, daemon):
            print("Calibrating...")
            daemon.state = Daemon.CalibrationState()

        def train_start(self, daemon, period):
            print("Training...")
            daemon.state = Daemon.TrainingState(period)

        def train_stop(self, daemon):
            raise Warning("Training hasn't been started.")

        def train_ambient_start(self, daemon):
            print("Ambient training...")
            daemon.state = Daemon.AmbientTrainingState()

        def train_ambient_stop(self, daemon):
            raise Warning("Ambient training hasn't been started.")

    class CalibrationState(State):

        def __init__(self):
            self.min_inputs = numpy.finfo(float).max
            self.max_inputs = numpy.finfo(float).min

        def step(self, daemon, mfcc_features):
            self.min_inputs = numpy.minimum(mfcc_features, self.min_inputs)
            self.max_inputs = numpy.maximum(mfcc_features, self.max_inputs)

        def calibrate_stop(self, daemon):
            daemon.network.set_input_scalings(
                numpy.reciprocal(self.max_inputs - self.min_inputs) * 0.2)
            daemon.network.set_input_bias(
                -(self.max_inputs + self.min_inputs) / 2.0)
            print("Free running...")
            daemon.state = Daemon.RunningState()

    class TrainingState(State):

        def __init__(self, period):
            self.stop_time = 0.0
            if period > 0.0:
                self.stop_time = time.time() + period
            self.end_time = 0.0
            self.train_value = 0.0

        def step(self, daemon, mfcc_features):
            daemon.network.set_inputs(mfcc_features)
            daemon.network.step(TIME_STEP)
            daemon.network.train_online([self.train_value])
            current_time = time.time()
            if self.stop_time > 0.0:
                if current_time >= self.stop_time:
                    self.train_stop(daemon)
                    self.stop_time = 0.0
            if self.end_time > 0.0:
                if current_time >= self.end_time:
                    print("Ambient training...")
                    daemon.state = Daemon.AmbientTrainingState()

        def train_start(self, daemon):
            raise Warning("Training has already been started.")

        def train_stop(self, daemon):
            self.train_value = PULSE_MAGNITUDE
            self.end_time = time.time() + PULSE_WIDTH

        def train_ambient_start(self, daemon):
            raise Warning("Cannot start ambient training while training.")

        def train_ambient_stop(self, daemon):
            raise Warning("Ambient training hasn't been started.")

    class AmbientTrainingState(State):

        def step(self, daemon, mfcc_features):
            daemon.network.set_inputs(mfcc_features)
            daemon.network.step(TIME_STEP)
            daemon.network.train_online([0.0])

        def train_start(self, daemon, period):
            print("Training...")
            daemon.state = Daemon.TrainingState(period)

        def train_ambient_stop(self, daemon):
            print("Free running...")
            daemon.state = Daemon.RunningState()
