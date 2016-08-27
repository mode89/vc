import input
import numpy
import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui

SAMPLE_RATE = 44100

pyqtgraph.setConfigOptions(antialias=True)

class Queue:

    def __init__(self, size):
        self.data = numpy.zeros(size)
        self.index = 0

    def extend(self, array):
        index = (self.index + numpy.arange(array.size)) % self.data.size
        self.data[index] = array
        self.index = index[-1] + 1

    def get(self):
        index = (self.index + numpy.arange(self.data.size)) % self.data.size
        return self.data[index]

class Window:

    def __init__(self):
        self.application = QtGui.QApplication([])
        self.window = pyqtgraph.GraphicsWindow()

    def addPlot(self, plot):
        self.window.addItem(plot)

    def isVisible(self):
        return self.window.isVisible()

    def update(self):
        self.application.processEvents()

class AudioPlot(pyqtgraph.PlotItem):

    BUFFER_LENGTH = 0.1

    def __init__(self):
        pyqtgraph.PlotItem.__init__(self)
        self.queue = Queue(SAMPLE_RATE * AudioPlot.BUFFER_LENGTH)
        self.samplesCounter = 0
        self.curve = self.plot()

    def appendSamples(self, samples):
        self.queue.extend(samples)
        self.curve.setData(self.queue.get())

if __name__ == "__main__":
    inputAudio = input.Audio()
    window = Window()
    audioPlot = AudioPlot()
    window.addPlot(audioPlot)
    while window.isVisible():
        samples = inputAudio.read_array()
        audioPlot.appendSamples(samples)
        window.update()
