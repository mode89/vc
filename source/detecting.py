import collections
import math

class RMS:

    def __init__(self, maxlen):
        self.queue = collections.deque(maxlen=int(maxlen))

    def append(self, value):
        self.queue.append(value)

    def __call__(self):
        total = sum(map(lambda x: x ** 2, self.queue))
        return math.sqrt(total / self.queue.maxlen)

class Pulse:

    def __init__(self, maxlen):
        # RMS value of a long sequence of values
        self.rms = RMS(maxlen * 10)
        # RMS value of a short sequence of values
        self.rmstemp = RMS(maxlen)
        # Current value of pulse
        self.value = False
        # True if begin of pulse detected
        self.begin = False
        # True if end of pulse detected
        self.end = False

    def update(self, value):
        self.rms.append(value)
        self.rmstemp.append(value)
        self.begin = False
        self.end = False
        if self.rmstemp() > self.rms():
            self.begin = True if not self.value else False
            self.value = True
        else:
            self.end = True if self.value else False
            self.value = False

class Error:
    """Error detector"""

    def __init__(self, maxlen, maxint):
        """Constructor

        Arguments:
        maxlen - number of samples for calculation of temporary RMS value
        maxint - maximum number of samples between corresponding reference
            and output pulses
        """
        self.ref = Pulse(maxlen)
        """Reference signal pulse detector"""
        self.out = Pulse(maxlen)
        """Output (real) signal pulse detector"""

    def update(self, ref, out):
        """Sample reference and output signals

        Arguments:
        ref - reference signal sample
        out - output signal sample
        """
        self.ref.update(ref)
        self.out.update(out)
