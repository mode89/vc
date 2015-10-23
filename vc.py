#!/usr/bin/python
import esn
import input

INPUT_COUNT = 13
NEURON_COUNT = 100
CONNECTIVITY = 0.5

def main():

    # Generate network

    print("Generating network...")
    network = esn.create_network(
        inputCount=INPUT_COUNT,
        neuronCount=NEURON_COUNT,
        outputCount=1,
        connectivity=CONNECTIVITY,
        useOrthonormalMatrix=True
    )

    input_audio = input.Audio()

    while True:
        network.set_inputs(input_audio.read())

    input.close()

if __name__ == "__main__":
    main()
