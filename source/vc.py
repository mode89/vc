import esn

NEURON_COUNT = 100
INPUT_COUNT = 100
CONNECTIVITY = 0.5

network = esn.create_network(
    inputCount=INPUT_COUNT,
    neuronCount=NEURON_COUNT,
    outputCount=1,
    connectivity=CONNECTIVITY,
    useOrthonormalMatrix=True
)
