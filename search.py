import detecting
import esn
from grid import Grid
import multiprocessing
import numpy
import training

SIM_STEP = 0.01
FREERUN_TIME = 1000.0

def simulation(neuron_count, connectivity, leaking_rate, input_scale,
    feedback_scale, washout_time, train_time):

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

    trainer = training.Trainer(network, washout_time=washout_time,
        train_time=train_time)

    stable = True
    error = detecting.Error(0.5 / SIM_STEP, 0.3 / SIM_STEP)
    try:
        while trainer.time < train_time:
            trainer.step(SIM_STEP)
        while trainer.time < (train_time + FREERUN_TIME):
            trainer.step(SIM_STEP)
            ref = trainer.outputs.value
            out = network.capture_output(1)[0]
            error.update(ref, out)
    except esn.OutputIsNotFinite:
        stable = False

    return trainer.time, stable, error.count

def simulation_star(params):
    time, stable, errcnt = simulation(**params)
    print(params)
    print("Time: {0}".format(time))
    print("Stable: {0}".format(stable))
    print("Error count: {0}".format(errcnt))

if __name__ == "__main__":

    grid = Grid(dict(
            neuron_count=[1000, 500, 100],
            connectivity=[0.5, 0.75, 1.0, 0.25],
            leaking_rate=[0.5, 0.1, 1.0],
            input_scale=[0.1, 0.01, 1.0],
            feedback_scale=[1.0, 0.1, 0.01],
            washout_time=[10.0, 50.0, 0.0],
            train_time=[500.0, 1000.0]
        ))

    pool = multiprocessing.Pool()
    pool.map(simulation_star, grid)
