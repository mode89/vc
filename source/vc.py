from collections import deque
from matplotlib import pyplot
from matplotlib import animation
import esn
import numpy
import training

NEURON_COUNT = 100
INPUT_COUNT = 100
CONNECTIVITY = 0.5
SIM_STEP = 0.01
TRAIN_TIME = 100.0
PLOT_TIME_WINDOW = 3.0
PLOT_EACH_NTH_AUDIO_FRAME = 20
SIM_STEPS_PER_ANIMATION_FRAME = 10
SIM_STEPS_PER_WINDOW = PLOT_TIME_WINDOW / SIM_STEP

# Create network

network = esn.create_network(
    inputCount=INPUT_COUNT,
    neuronCount=NEURON_COUNT,
    outputCount=1,
    connectivity=CONNECTIVITY,
    useOrthonormalMatrix=True
)

# Train the network

trainer = training.Trainer(network)

figure = pyplot.figure()
plot_audio = pyplot.subplot(211)
plot_mfcc = pyplot.subplot(212)
audio_line, = plot_audio.plot([], [])
plot_audio.set_ylim(-0.2, 0.2)
plot_audio.grid(True)
image_mfcc = pyplot.imshow(numpy.empty([13, SIM_STEPS_PER_WINDOW]),
    interpolation="gaussian", aspect="auto", cmap="gist_ncar")
image_mfcc.set_extent((0, 100, 13, 0))
image_mfcc.set_clim(-25.0, 3.0)

time_data = deque()
audio_data = deque()
mfcc_data = numpy.empty([13, SIM_STEPS_PER_WINDOW])

def animation_function(animation_frame):
    animation_time = animation_frame * SIM_STEP * \
        SIM_STEPS_PER_ANIMATION_FRAME
    for i in range(SIM_STEPS_PER_ANIMATION_FRAME):
        trainer.step(SIM_STEP)
        audio_frames = trainer.inputs.frames
        audio_frame_time = SIM_STEP / len(audio_frames)
        plot_audio_frames_count = PLOT_TIME_WINDOW / \
            (audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME)
        for audio_frame in \
                trainer.inputs.frames[::PLOT_EACH_NTH_AUDIO_FRAME]:
            time_data.append(animation_time)
            if len(time_data) > plot_audio_frames_count:
                time_data.popleft()
            animation_time += audio_frame_time * PLOT_EACH_NTH_AUDIO_FRAME
            audio_data.append(audio_frame)
            if len(audio_data) > plot_audio_frames_count:
                audio_data.popleft()
        global mfcc_data
        mfcc_data = numpy.roll(mfcc_data, -1)
        mfcc_data[:,-1] = trainer.inputs.mfcc
    audio_line.set_data(time_data, audio_data)
    plot_audio.set_xlim(animation_time - PLOT_TIME_WINDOW, animation_time)
    image_mfcc.set_array(mfcc_data)
    image_mfcc.set_extent(
        (animation_time - PLOT_TIME_WINDOW, animation_time, 13, 0))

animation_object = animation.FuncAnimation(figure, animation_function,
    interval=100)

pyplot.show()
