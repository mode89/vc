from collections import deque
from matplotlib import pyplot
from matplotlib import animation
from multiprocessing import Process
import numpy

SIM_STEP = 0.01
PLOT_TIME_WINDOW = 3.0
PLOT_EACH_NTH_AUDIO_FRAME = 20
SIM_STEPS_PER_ANIMATION_FRAME = 10
SIM_STEPS_PER_WINDOW = PLOT_TIME_WINDOW / SIM_STEP

class Plot(Process):

    def __init__(self, trainer):
        Process.__init__(self)
        self.trainer = trainer

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
            Plot.animation_function, fargs=[self], interval=100)

        pyplot.show()

    @staticmethod
    def animation_function(animation_frame, plot):
        animation_time = animation_frame * SIM_STEP * \
            SIM_STEPS_PER_ANIMATION_FRAME
        for i in range(SIM_STEPS_PER_ANIMATION_FRAME):
            plot.trainer.step(SIM_STEP)
            audio_frames = plot.trainer.inputs.frames
            audio_frame_time = SIM_STEP / len(audio_frames)
            plot_audio_frames_count = PLOT_TIME_WINDOW / \
                (audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME)
            for audio_frame in \
                    plot.trainer.inputs.frames[
                        ::PLOT_EACH_NTH_AUDIO_FRAME]:
                plot.time_data.append(animation_time)
                if len(plot.time_data) > plot_audio_frames_count:
                    plot.time_data.popleft()
                animation_time += \
                    audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME
                plot.audio_data.append(audio_frame)
                if len(plot.audio_data) > plot_audio_frames_count:
                    plot.audio_data.popleft()
            plot.mfcc_data = numpy.roll(plot.mfcc_data, -1)
            plot.mfcc_data[:,-1] = plot.trainer.inputs.mfcc
        plot.audio_line.set_data(plot.time_data, plot.audio_data)
        plot.plot_audio.set_xlim(
            animation_time - PLOT_TIME_WINDOW, animation_time)
        plot.image_mfcc.set_array(plot.mfcc_data)
        plot.image_mfcc.set_extent(
            (animation_time - PLOT_TIME_WINDOW, animation_time, 13, 0))
