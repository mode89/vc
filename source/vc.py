import esn
import plotting
import training

NEURON_COUNT = 100
INPUT_COUNT = 100
CONNECTIVITY = 0.5
SIM_STEP = 0.01
TRAIN_TIME = 100.0

# Create network

network = esn.create_network(
    inputCount=INPUT_COUNT,
    neuronCount=NEURON_COUNT,
    outputCount=1,
    connectivity=CONNECTIVITY,
    useOrthonormalMatrix=True
)

# Train the network

trainer = training.Trainer(network)
plot = plotting.Plot(trainer)
plot.start()

while plot.is_alive():
    trainer.step(SIM_STEP)
    plot.update()
