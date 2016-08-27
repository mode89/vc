import input
import pickle
import random
import time
import zipfile

PROMPT_PAUSE_MIN = 2
PROMPT_PAUSE_MAX = 5

WORDS = [
    "One",
    "Two",
    "Three"
]

WORD_ENTRY_NUMBER = 10

class Data:
    def __init__(self):
        self.time = None
        self.frames = None
        self.mark = { word: False for word in WORDS }

if __name__ == "__main__":
    print("Opening audio input...")
    audio = input.Audio()

    print("Capturing...")
    random_word = random.Random()
    random_pause = random.Random()
    output_file = zipfile.ZipFile("captured.pkl.zip", mode="a")
    orig_time = time.time()
    prompt_time = random_pause.uniform(PROMPT_PAUSE_MIN, PROMPT_PAUSE_MAX)
    word_count = dict()
    while True:
        cur_time = time.time() - orig_time
        data = Data()
        data.time = cur_time
        data.frames = audio.read()

        if cur_time >= prompt_time:
            need_continue = False
            for word in WORDS:
                if word in word_count:
                    if word_count[word] < WORD_ENTRY_NUMBER:
                        need_continue = True
                else:
                    need_continue = True
            if not need_continue: break

            word = random_word.choice(WORDS)

            print(word)
            data.mark[word] = True
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 0

            prompt_time = prompt_time + random_pause.uniform(
                PROMPT_PAUSE_MIN, PROMPT_PAUSE_MAX)

        output_file.writestr("captured.pkl", pickle.dumps(data))
