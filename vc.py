import esn
import numpy
import plotting
import time
import training

NEURON_COUNT = 100
INPUT_COUNT = 13
CONNECTIVITY = 0.5
SIM_STEP = 0.01
SLEEP_TIME = 0.02
NORMALIZE_TIME = 50.0
WASHOUT_TIME = 50.0
TRAIN_TIME = 300.0

if __name__ == "__main__":

    # Create network

    print("Generating network...")
    network = esn.create_network(
        inputCount=INPUT_COUNT,
        neuronCount=NEURON_COUNT,
        outputCount=1,
        connectivity=CONNECTIVITY,
        useOrthonormalMatrix=True
    )

    # Train the network

    trainer = training.Trainer(network, washout_time=WASHOUT_TIME,
        train_time=TRAIN_TIME)

    # Calculate input scalings
    print("Normalizing inputs...")
    inmin = numpy.finfo(float).max
    inmax = numpy.finfo(float).min
    for i in range(int(NORMALIZE_TIME / SIM_STEP)):
        inputs = trainer.inputs
        inputs.update(SIM_STEP)
        inmin = numpy.minimum(inmin, inputs())
        inmax = numpy.maximum(inmax, inputs())
    network.set_input_scalings(numpy.reciprocal(inmax - inmin) * 0.2)
    network.set_input_bias(-(inmax + inmin) / 2.0)

    # No need to plot during washing out
    print("Washing-out...")
    while trainer.time < WASHOUT_TIME:
        trainer.step(SIM_STEP)

    print("Training...")
    plot = plotting.Plot(trainer)
    plot.start()
    while plot.is_alive():
        trainer.step(SIM_STEP)
        plot.update()
        time.sleep(SLEEP_TIME)
