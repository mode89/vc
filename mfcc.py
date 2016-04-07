import scikits.talkbox.features as scikits

FRAME_RATE = 44100

def mfcc(frames, num_coeff):
    return scikits.mfcc(frames, fs=FRAME_RATE, nceps=num_coeff)[0][0]
