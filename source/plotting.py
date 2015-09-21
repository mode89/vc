from collections import deque
from detecting import RMS
from matplotlib import pyplot
from matplotlib import animation
from multiprocessing import Process, Queue
import numpy
from Queue import Full

SIM_STEP = 0.01
PLOT_TIME_WINDOW = 3.0
PLOT_EACH_NTH_AUDIO_FRAME = 20
SIM_STEPS_PER_WINDOW = PLOT_TIME_WINDOW / SIM_STEP

class Data:

    time = None
    frames = None
    mfcc = None
    output = None

class Plot(Process):

    def __init__(self, trainer):
        Process.__init__(self)
        self.trainer = trainer
        self.queue = Queue(1)
        self.network_output_rms = RMS(50)

    def update(self):
        try:
            data = Data()
            data.time = self.trainer.time
            data.frames = self.trainer.inputs.frames
            data.mfcc = self.trainer.inputs.mfcc
            data.output = self.trainer.outputs.value
            data.network_output = self.trainer.network.capture_output(1)[0]
            self.network_output_rms.append(data.network_output)
            data.network_output_rms = self.network_output_rms() * 5
            self.queue.put_nowait(data)
        except Full: pass

    def run(self):
        self.figure = pyplot.figure()

        self.plot_audio = pyplot.subplot(311)
        self.plot_mfcc = pyplot.subplot(312)
        self.plot_output = pyplot.subplot(313)

        self.audio_line, = self.plot_audio.plot([], [])
        self.plot_audio.set_ylim(-0.2, 0.2)
        self.plot_audio.grid(True)

        self.image_mfcc = self.plot_mfcc.imshow(
            numpy.empty([13, SIM_STEPS_PER_WINDOW]),
            interpolation="gaussian", aspect="auto", cmap="gist_ncar")
        self.image_mfcc.set_extent((0, 100, 13, 0))
        self.image_mfcc.set_clim(-25.0, 3.0)

        self.line_output, = self.plot_output.plot([], [])
        self.line_network_output, = self.plot_output.plot([], [])
        self.line_network_output_rms, = self.plot_output.plot([], [])
        self.plot_output.set_ylim(-0.1, 1.1)
        self.plot_output.grid(True)

        self.time_data = deque()
        self.audio_data = deque()
        self.output_time_data = deque()
        self.output_data = deque()
        self.network_output_data = deque()
        self.network_output_rms_data = deque()
        self.mfcc_data = numpy.zeros([13, SIM_STEPS_PER_WINDOW])

        animation_object = animation.FuncAnimation(self.figure,
            lambda frame_id: self.animation(), interval=30)

        pyplot.show()

    def animation(self):
        data = self.queue.get_nowait()
        time = data.time
        audio_frame_time = SIM_STEP / len(data.frames)
        plot_audio_frames_count = PLOT_TIME_WINDOW / \
            (audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME)
        for audio_frame in data.frames[::PLOT_EACH_NTH_AUDIO_FRAME]:
            self.time_data.append(time)
            if len(self.time_data) > plot_audio_frames_count:
                self.time_data.popleft()
            time += audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME
            self.audio_data.append(audio_frame)
            if len(self.audio_data) > plot_audio_frames_count:
                self.audio_data.popleft()
        self.mfcc_data = numpy.roll(self.mfcc_data, -1)
        self.mfcc_data[:,-1] = data.mfcc
        self.audio_line.set_data(self.time_data, self.audio_data)
        self.plot_audio.set_xlim(
            time - PLOT_TIME_WINDOW, time)
        self.image_mfcc.set_array(self.mfcc_data)
        self.image_mfcc.set_extent(
            (time - PLOT_TIME_WINDOW, time, 13, 0))

        self.output_time_data.append(data.time)
        if len(self.output_time_data) > 100:
            self.output_time_data.popleft()
        self.output_data.append(data.output)
        if len(self.output_data) > 100:
            self.output_data.popleft()
        self.line_output.set_data(
            self.output_time_data, self.output_data)
        self.plot_output.set_xlim(data.time - PLOT_TIME_WINDOW, data.time)

        self.network_output_data.append(data.network_output)
        if len(self.network_output_data) > 100:
            self.network_output_data.popleft()
        self.line_network_output.set_data(
            self.output_time_data, self.network_output_data)

        self.network_output_rms_data.append(data.network_output_rms)
        if len(self.network_output_rms_data) > 100:
            self.network_output_rms_data.popleft()
        self.line_network_output_rms.set_data(
            self.output_time_data, self.network_output_rms_data)
