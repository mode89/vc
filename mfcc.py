import scikits.talkbox.features as scikits

FRAME_RATE = 44100
COEFF_NUM = 13

def mfcc(frames):
    return scikits.mfcc(frames, fs=FRAME_RATE, nceps=COEFF_NUM)[0][0]
