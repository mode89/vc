from collections import deque
from matplotlib import pyplot
from matplotlib import animation
from multiprocessing import Process, Queue
import numpy

SIM_STEP = 0.01
PLOT_TIME_WINDOW = 3.0
PLOT_EACH_NTH_AUDIO_FRAME = 20
SIM_STEPS_PER_WINDOW = PLOT_TIME_WINDOW / SIM_STEP

class Data:

    time = None
    frames = None
    mfcc = None

class Plot(Process):

    def __init__(self, trainer):
        Process.__init__(self)
        self.trainer = trainer
        self.queue = Queue(1)

    def update(self):
        try:
            data = Data()
            data.time = self.trainer.time
            data.frames = self.trainer.inputs.frames
            data.mfcc = self.trainer.inputs.mfcc
            self.queue.put_nowait(data)
        except: pass

    def run(self):
        self.figure = pyplot.figure()
        self.plot_audio = pyplot.subplot(211)
        self.plot_mfcc = pyplot.subplot(212)
        self.audio_line, = self.plot_audio.plot([], [])
        self.plot_audio.set_ylim(-0.2, 0.2)
        self.plot_audio.grid(True)
        self.image_mfcc = self.plot_mfcc.imshow(
            numpy.empty([13, SIM_STEPS_PER_WINDOW]),
            interpolation="gaussian", aspect="auto", cmap="gist_ncar")
        self.image_mfcc.set_extent((0, 100, 13, 0))
        self.image_mfcc.set_clim(-25.0, 3.0)

        self.time_data = deque()
        self.audio_data = deque()
        self.mfcc_data = numpy.zeros([13, SIM_STEPS_PER_WINDOW])

        animation_object = animation.FuncAnimation(self.figure,
            Plot.animation_function, fargs=[self], interval=30)

        pyplot.show()

    @staticmethod
    def animation_function(animation_frame, plot):
        data = plot.queue.get_nowait()
        time = data.time
        audio_frame_time = SIM_STEP / len(data.frames)
        plot_audio_frames_count = PLOT_TIME_WINDOW / \
            (audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME)
        for audio_frame in data.frames[::PLOT_EACH_NTH_AUDIO_FRAME]:
            plot.time_data.append(time)
            if len(plot.time_data) > plot_audio_frames_count:
                plot.time_data.popleft()
            time += audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME
            plot.audio_data.append(audio_frame)
            if len(plot.audio_data) > plot_audio_frames_count:
                plot.audio_data.popleft()
        plot.mfcc_data = numpy.roll(plot.mfcc_data, -1)
        plot.mfcc_data[:,-1] = data.mfcc
        plot.audio_line.set_data(plot.time_data, plot.audio_data)
        plot.plot_audio.set_xlim(
            time - PLOT_TIME_WINDOW, time)
        plot.image_mfcc.set_array(plot.mfcc_data)
        plot.image_mfcc.set_extent(
            (time - PLOT_TIME_WINDOW, time, 13, 0))
