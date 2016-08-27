import pyaudio
import soundfile

def blocks(frames, blocksize):
    for i in range(0, len(frames), blocksize):
        yield frames[i : i + blocksize]

if __name__ == "__main__":
    with soundfile.SoundFile("computer.ogg") as soundFile:
        print(soundFile)
        length = soundFile.seek(0, soundfile.SEEK_END)
        soundFile.seek(0)
        frames = soundFile.read(frames=length, dtype="int16")

        audio = pyaudio.PyAudio()
        outputStream = audio.open(
            format=pyaudio.paInt16,
            channels=soundFile.channels,
            rate=soundFile.samplerate,
            output=True)

        chunkSize = soundFile.samplerate / 10
        for block in blocks(frames, chunkSize):
            outputStream.write(block, chunkSize)
