import math
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import threading
import wave

NOISE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
BAR_COUNT = 100
SAMPLE_RATE = 100

noise = wave.open( NOISE_PATH, "r" )
frame_rate = noise.getframerate()
FRAMES_PER_SAMPLE = int( frame_rate / SAMPLE_RATE )
frames = []
for i in range( noise.getnframes() ) :
    frame = noise.readframes( 1 )
    frames.append( struct.unpack( "<h", frame ) )

class Worker( threading.Thread ) :

    def __init__( self ) :
        threading.Thread.__init__( self )
        self._event_stop = threading.Event()

    def run( self ) :
        while not self._event_stop.isSet():
            for i in range( 0, noise.getnframes(), FRAMES_PER_SAMPLE ) :
                self.fft = np.fft.fft(
                    frames[ i : i + FRAMES_PER_SAMPLE ], axis=0 )

    def stop( self ) :
        self._event_stop.set()

worker = Worker()
worker.start()

freq = np.fft.fftfreq( FRAMES_PER_SAMPLE, 1.0 / frame_rate )
ft = np.fft.fft( frames[ 0 : FRAMES_PER_SAMPLE ], axis=0 )

figure = plt.figure()
plotBars = plt.bar(
    # left=map( math.log10, freq[ 1 : BAR_COUNT ] ),
    left = freq[ 1 : BAR_COUNT ],
    height=list( map( abs, ft[ 1 : BAR_COUNT ] ) ),
    align="center", width=0.01 )
plt.ylim(10, 300000)

def animateFunction( sampleId ) :
    for i, bar in enumerate( plotBars ) :
        bar.set_height( abs( worker.fft[i + 1] ) )

anim = animation.FuncAnimation( figure, animateFunction, interval=100 )

plt.show()

worker.stop()
worker.join()
