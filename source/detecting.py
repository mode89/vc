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
        self.maxint = maxint
        """Maximum number of samples between correspoinding reference and
            output pulses"""
        self.state = Error.Updating(self)
        """Current state of the error detector"""
        self.detected = False
        """True if an error has been detected during the last update"""

    def update(self, ref, out):
        """Sample reference and output signals

        Arguments:
        ref - reference signal sample
        out - output signal sample
        """
        self.ref.update(ref)
        self.out.update(out)
        self.detected = False
        self.state = self.state.next()

    class Updating:
        """Updating state of reference and output pulse detectors"""

        def __init__(self, context):
            """Save reference to error detector object

            Arguments:
            context - Error detector object
            """
            self.context = context
            """Error detector object"""

        def next(self):
            """Determine the next state of the error detector"""
            if self.context.ref.begin and self.context.out.begin:
                return self
            elif self.context.ref.begin:
                return Error.WaitingOut(self.context)
            elif self.context.out.begin:
                return Error.WaitingRef(self.context)
            else:
                return self

    class WaitingRef:
        """Waiting for a pulse of reference signal"""

        def __init__(self, context):
            """Save reference to error detector object and initialize
            countdown

            Arguments:
            context - Error detector object
            """
            self.context = context
            """Error detector object"""
            self.countdown = context.maxint
            """Count down samples until pulse of reference signal"""

        def next(self):
            """Determine the next state of the error detector"""
            if self.countdown == 0:
                self.context.detected = True
                return Error.Updating(self.context)
            elif self.context.out.begin:
                self.context.detected = True
                # Restart waiting if two consecutive pulses of the same
                # signal have came
                return Error.WaitingRef(self.context)
            elif self.context.ref.begin:
                return Error.Updating(self.context)
            else:
                self.countdown -= 1
                return self

    class WaitingOut:
        """Waiting for a pulse of output signal"""

        def __init__(self, context):
            """Save reference to error detector object and initialize
            countdown

            Arguments:
            context - Error detector object
            """
            self.context = context
            """Error detector object"""
            self.countdown = context.maxint
            """Count down samples until pulse of output signal"""

        def next(self):
            """Determine the next state of the error detector"""
            if self.countdown == 0:
                self.context.detected = True
                return Error.Updating(self.context)
            elif self.context.ref.begin:
                self.context.detected = True
                # Restart waiting if two consecutive pulses of the same
                # signal have came
                return Error.WaitingOut(self.context)
            elif self.context.out.begin:
                return Error.Updating(self.context)
            else:
                self.countdown -= 1
                return self
