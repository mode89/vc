import esn
import numpy
import training

SIM_STEP = 0.01

class Model:

    def __init__(self, neuron_count, connectivity, leaking_rate,
        input_scale, feedback_scale, washout_time, train_time):

        network = esn.create_network(
            inputCount=13,
            neuronCount=neuron_count,
            outputCount=1,
            connectivity=connectivity,
            leakingRate=leaking_rate,
            useOrthonormalMatrix=True)

        input_scalings = numpy.ones(13) * input_scale
        input_scalings[0] *= 0.03
        network.set_input_scalings(input_scalings)
        network.set_feedback_scalings([feedback_scale])

        self.trainer = training.Trainer(network, washout_time=washout_time,
            train_time=train_time)

    def run(self):
        while self.trainer.time < self.trainer.train_time:
            self.trainer.step(SIM_STEP)
