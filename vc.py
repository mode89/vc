import esn
import pyaudio

INPUT_COUNT = 13
NEURON_COUNT = 100
CONNECTIVITY = 0.5

INPUT_FORMAT = pyaudio.paInt16
FRAME_RATE = 44100
SAMPLE_RATE = 100

def capture_callback(in_data, frame_count, time_info, status_flag):
    return in_data, pyaudio.paContinue

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

    p = pyaudio.PyAudio()
    stream = p.open(
        input=True,
        format=INPUT_FORMAT,
        channels=1,
        rate=FRAME_RATE,
        frames_per_buffer=FRAME_RATE / SAMPLE_RATE,
        stream_callback=capture_callback)
    stream.start_stream()
    stream.stop_stream()
    stream.close()

if __name__ == "__main__":
    main()
