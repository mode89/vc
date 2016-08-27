from plotting import MfccGraph, OutputGraph, Plot
import esn
import input
import mfcc
import signals

NEURON_COUNT = 512
CONNECTIVITY = 0.5
MFCC_COEFF = 13

def read_coeffs():
    return mfcc.mfcc(audio.read(), num_coeff=MFCC_COEFF)

class Trainer:

    def __init__(self):
        self.noise = signals.PerlinNoise(persistence=0.3, octave_count=7)
        self.trigger = signals.TriggerWithDelayedOff(on=1.0, delay=100)

    def update(self, time):
        self.noise_value = self.noise(time * 0.1)
        self.trigger.update(self.noise_value)
        self.state = self.trigger.switched_on or self.trigger.switched_off
        self.output = 0.7 if self.trigger.switched_off else 0

if __name__ == "__main__":

    print("Generating network...")
    params = esn.NetworkParamsNSLI()
    params.inputCount = MFCC_COEFF
    params.neuronCount = NEURON_COUNT
    params.outputCount = 1
    params.hasOutputFeedback = False
    params.connectivity = CONNECTIVITY
    network = esn.CreateNetwork(params)

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

    print("Training...")
    plot = Plot()
    plot.mfcc = MfccGraph(MFCC_COEFF)
    plot.add(plot.mfcc)
    plot.out = OutputGraph()
    plot.add(plot.out)
    plot.say = OutputGraph()
    plot.add(plot.say)
    plot.out_ref = OutputGraph()
    plot.add(plot.out_ref)
    plot.start()
    trainer = Trainer()
    while plot.is_alive():
        coeffs = read_coeffs()
        network.set_inputs(coeffs)
        network.step(1.0)
        norm_coeffs = network.capture_transformed_inputs(MFCC_COEFF)
        output = network.capture_output(1)
        trainer.update(time)
        network.train_online([trainer.output], forceOutput=False)
        #print(output[0])
        plot.mfcc.append(norm_coeffs, time)
        plot.out.append(output[0], time)
        plot.say.append(0.7 if trainer.trigger.switched_on else 0, time)
        #plot.out.append(trainer.noise_value, time)
        plot.out_ref.append(trainer.output, time)
        #plot.out_ref.append(trainer.noise_value, time)
        time += 1

    audio.close()
