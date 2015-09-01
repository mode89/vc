import esn
from grid import Grid
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

if __name__ == "__main__":

    grid = Grid(dict(
            neuron_count=[1000, 500, 100],
            connectivity=[0.5, 0.75, 1.0, 0.25],
            leaking_rate=[0.5, 0.1, 1.0],
            input_scale=[0.1, 0.01, 1.0],
            feedback_scale=[1.0, 0.1, 0.01],
            washout_time=[10.0, 50.0, 0.0],
            train_time=[500.0, 1000.0, 100.0]
        ))

    for params in grid:
        print(params)
        model = Model(**params)
        model.run()
