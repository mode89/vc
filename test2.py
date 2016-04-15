from plotting import MfccGraph, OutputGraph, Plot
import esn
import input
import mfcc

NEURON_COUNT = 256
CONNECTIVITY = 0.5
MFCC_COEFF = 13

def read_coeffs():
    return mfcc.mfcc(audio.read(), num_coeff=MFCC_COEFF)

if __name__ == "__main__":

    print("Generating network...")
    network = esn.Network(
        ins=MFCC_COEFF,
        neurons=NEURON_COUNT,
        outs=1,
        has_ofb=False,
        cnctvty=CONNECTIVITY
    )

    print("Opening audio input...")
    audio = input.Audio()

    print("Normalizing inputs...")
    plot = Plot()
    plot.mfcc = MfccGraph(MFCC_COEFF)
    plot.add(plot.mfcc)
    plot.start()
    min_values = [float("inf")] * MFCC_COEFF
    max_values = [float("-inf")] * MFCC_COEFF
    time = 0
    while plot.is_alive():
        coeffs = read_coeffs()
        plot.mfcc.append(coeffs, time)
        time += 1
        for i in range(MFCC_COEFF):
            min_values[i] = min(coeffs[i], min_values[i])
            max_values[i] = max(coeffs[i], max_values[i])

    input_scaling = [2.0 / (max_values[i] - min_values[i])
        for i in range(MFCC_COEFF)]
    input_bias = [-0.5 * (max_values[i] + min_values[i])
        for i in range(MFCC_COEFF)]

    network.set_input_scalings(input_scaling)
    network.set_input_bias(input_bias)

    print("Washing out...")
    plot = Plot()
    plot.mfcc = MfccGraph(MFCC_COEFF)
    plot.add(plot.mfcc)
    plot.out = OutputGraph()
    plot.add(plot.out)
    plot.start()
    while plot.is_alive():
        coeffs = read_coeffs()
        network.set_inputs(coeffs)
        network.step(1.0)
        norm_coeffs = network.capture_transformed_inputs(MFCC_COEFF)
        output = network.capture_output(1)
        print(output[0])
        plot.mfcc.append(norm_coeffs, time)
        plot.out.append(output[0], time)
        time += 1

    audio.close()
