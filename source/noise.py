import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import wave

NOISE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
BAR_COUNT = 100
SAMPLE_RATE = 100

noise = wave.open( NOISE_PATH, "r" )
frame_rate = noise.getframerate()
FRAMES_PER_SAMPLE = frame_rate / SAMPLE_RATE
frames = []
for i in range( noise.getnframes() ) :
    frame = noise.readframes( 1 )
    frames.append( struct.unpack( "<h", frame ) )

freq = np.fft.fftfreq( FRAMES_PER_SAMPLE, 1.0 / frame_rate )
ft = np.fft.fft( frames[ 0 : FRAMES_PER_SAMPLE ], axis=0 )

figure = plt.figure()
plotBars = plt.bar(
    # left=map( math.log10, freq[ 1 : BAR_COUNT ] ),
    left = freq[ 1 : BAR_COUNT ],
    height=map( abs, ft[ 1 : BAR_COUNT ] ),
    align="center", width=0.01 )
plt.ylim(10, 300000)

def animateFunction( sampleId ) :
    first_frame = sampleId * FRAMES_PER_SAMPLE
    last_frame = first_frame + FRAMES_PER_SAMPLE
    fft = np.fft.fft( frames[ first_frame : last_frame ], axis = 0 )
    for i, bar in enumerate( plotBars ) :
        bar.set_height( abs( fft[i + 1] ) )

anim = animation.FuncAnimation( figure, animateFunction,
    frames=len( frames ) / FRAMES_PER_SAMPLE, interval=30 )

plt.show()
