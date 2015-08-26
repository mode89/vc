import numpy as np
import os
import struct
import wave

WAVE_FILE_PATH = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), "data/noise.wav" )
SAMPLE_RATE = 100

class Model :

    def __init__( self ) :

        # Read wavefront file

        wave_file = wave.open( WAVE_FILE_PATH, "r" )
        frame_rate = wave_file.getframerate()
        frame_count = wave_file.getnframes()
        frames = np.fromstring( string=wave_file.readframes( frame_count ),
            dtype=np.int16 ) / float( np.iinfo( np.int16 ).max )
        frames_per_sample = int( frame_rate / SAMPLE_RATE )
        fft_freq_count = frames_per_sample / 2

        # Find minimums and maximums of FFT

        self.fft_min = np.full( fft_freq_count - 1, np.Inf )
        self.fft_max = np.zeros( fft_freq_count - 1 )

        frame_range = range( 0, frame_count - frames_per_sample,
            frames_per_sample )
        for first_frame in frame_range:
            last_frame = first_frame + frames_per_sample
            fft = np.fft.fft( frames[ first_frame : last_frame ], axis=0 )
            abs_fft = np.abs( fft[ 1 : fft_freq_count ] ) / \
                frames_per_sample
            self.fft_min = np.minimum( self.fft_min, abs_fft )
            self.fft_max = np.maximum( self.fft_max, abs_fft )
