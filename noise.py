import numpy as np
import os
import struct
import wave

WAVE_FILE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )

class Model :

    def __init__( self ) :

        # Read wavefront file

        wave_file = wave.open( WAVE_FILE_PATH, "r" )
        frame_count = wave_file.getnframes()
        frames = np.fromstring( string=wave_file.readframes( frame_count ),
            dtype=np.int16 ) / float( np.iinfo( np.int16 ).max )
        wave_file.close()
