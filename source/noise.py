import os
import struct
import wave

NOISE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
noise = wave.open( NOISE_PATH, "r" )
frames = []
for i in range( noise.getnframes() ) :
    frame = noise.readframes( 1 )
    frames.append( struct.unpack( "<h", frame ) )
