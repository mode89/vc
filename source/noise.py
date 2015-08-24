import os
import wave

NOISE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
noise = wave.open( NOISE_PATH, "r" )
