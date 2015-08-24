import math
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import wave

NOISE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
noise = wave.open( NOISE_PATH, "r" )
frame_rate = noise.getframerate()
frames = []
for i in range( noise.getnframes() ) :
    frame = noise.readframes( 1 )
    frames.append( struct.unpack( "<h", frame ) )
ft = np.fft.fft( frames[ 0 : ( frame_rate / 10 ) ], axis=0 )
freq = np.fft.fftfreq( len( ft ), 1.0 / frame_rate )
plt.bar(
    left=map( math.log10, freq[ 1 : 100 ] ),
    height=map( abs, ft[ 1 : 100 ] ),
    align="center", width=0.1 )
plt.show()
