from collections import deque
from detecting import RMS
from matplotlib import pyplot
from matplotlib import animation
from multiprocessing import Process, Queue
import numpy
from Queue import Full

class Plot(Process):

    def __init__(self):
        Process.__init__(self)
        self.graphs = list()

    def add(self, graph):
        self.graphs.append(graph)

    def run(self):
        self.figure = pyplot.figure()
        for i in range(len(self.graphs)):
            subplot = pyplot.subplot(len(self.graphs), 1, i + 1)
            self.graphs[i].show(self.figure, subplot)
        pyplot.show()

class MfccData:
    time = None
    coeffs = None

class MfccGraph:

    def __init__(self, num_coeff):
        self.queue = Queue()
        self.num_coeff = num_coeff

    def append(self, coeffs, time):
        data = MfccData()
        data.time = time
        data.coeffs = coeffs
        self.queue.put_nowait(data)

    def show(self, figure, subplot):
        self.subplot = subplot
        self.data = numpy.zeros([self.num_coeff, 100])
        self.time = deque(maxlen=100)
        self.image = self.subplot.imshow(self.data,
            interpolation="gaussian", aspect="auto")
        self.image.set_extent((0, 100, self.num_coeff, 0))
        self.image.set_clim(0.0, 1.0)

        self.anim = animation.FuncAnimation(figure,
            lambda frame_id: self.animation(), interval=100)

    def animation(self):
        while not self.queue.empty():
            data = self.queue.get_nowait()
            self.data = numpy.roll(self.data, -1)
            self.data[:,-1] = data.coeffs
            self.time.append(data.time)
        self.image.set_array(self.data)
        self.image.set_extent(
            (self.time[0], self.time[-1], self.num_coeff, 0))
