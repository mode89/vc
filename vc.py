#!/usr/bin/python
import argparse
import esn
import input

INPUT_COUNT = 13
NEURON_COUNT = 100
CONNECTIVITY = 0.5

COMMANDS = ["daemonize"]

def daemonize():
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
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "command", metavar="<command>", choices=COMMANDS,
        help="Execute command.")
    args = argparser.parse_args()
    locals()[args.command]()
