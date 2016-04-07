import esn
import input
import mfcc
import plotting

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
    mfcc_plot = plotting.PlotMFCC(num_coeff=MFCC_COEFF)
    min_values = [float("inf")] * MFCC_COEFF
    max_values = [float("-inf")] * MFCC_COEFF
    time = 0
    while mfcc_plot.is_alive():
        coeffs = read_coeffs()
        mfcc_plot.append(coeffs, time)
        time += 1
        for i in range(MFCC_COEFF):
            min_values[i] = min(coeffs[i], min_values[i])
            max_values[i] = max(coeffs[i], max_values[i])

    input_scaling = [1.0 / (max_values[i] - min_values[i])
        for i in range(MFCC_COEFF)]
    input_bias = [-0.5 * (max_values[i] - min_values[i])
        for i in range(MFCC_COEFF)]

    network.set_input_scalings(input_scaling)
    network.set_input_bias(input_bias)

    audio.close()
