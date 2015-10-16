import pyaudio

INPUT_FORMAT = pyaudio.paInt16
FRAME_RATE = 44100
SAMPLE_RATE = 100

def capture_callback(in_data, frame_count, time_info, status_flag):
    return in_data, pyaudio.paContinue

def main():
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
