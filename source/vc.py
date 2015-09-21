import esn
import plotting
import time
import training

NEURON_COUNT = 100
INPUT_COUNT = 13
CONNECTIVITY = 0.5
SIM_STEP = 0.01
SLEEP_TIME = 0.02
WASHOUT_TIME = 50.0
TRAIN_TIME = 300.0

if __name__ == "__main__":

    # Create network

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

    # No need to plot during washing out
    while trainer.time < WASHOUT_TIME:
        trainer.step(SIM_STEP)

    plot = plotting.Plot(trainer)
    plot.start()
    while plot.is_alive():
        trainer.step(SIM_STEP)
        plot.update()
        time.sleep(SLEEP_TIME)
