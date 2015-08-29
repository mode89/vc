from collections import deque
from matplotlib import pyplot
from matplotlib import animation
import esn
import training

NEURON_COUNT = 100
INPUT_COUNT = 100
CONNECTIVITY = 0.5
SIM_STEP = 0.01
TRAIN_TIME = 100.0
PLOT_TIME_WINDOW = 1.0
PLOT_EACH_NTH_AUDIO_FRAME = 20
SIM_STEPS_PER_ANIMATION_FRAME = 30

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
audio_line, = pyplot.plot([], [])
pyplot.ylim(-0.2, 0.2)
pyplot.grid(True)

time_data = deque()
audio_data = deque()

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
    audio_line.set_data(time_data, audio_data)
    pyplot.xlim(animation_time - PLOT_TIME_WINDOW, animation_time)

animation_object = animation.FuncAnimation(figure, animation_function,
    interval=100)

pyplot.show()
