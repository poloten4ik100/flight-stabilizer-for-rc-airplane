from multiprocessing import Process, current_process, Queue
import time
import json

from control import Control

from serialReader import reader

FILE = "controller.json"

TIME_LIMIT = 30  # time of calibration in seconds


def calibration(proc: Process, queue: Queue, no_save: bool = False):

    start_time = time.time()

    result = {}

    angles = {i: Control() for i in range(1, 7)}

    while proc.is_alive() and time.time() - start_time <= TIME_LIMIT:

        while not queue.empty():

            chan, val = queue.get()

            angles[chan].setup(val)
            result.update({chan: (angles[chan].min, angles[chan].max)})

            print(int(TIME_LIMIT - (time.time() - start_time)), end=" | ")
            for i in range(1, 7):
                if i in result:
                    print(i, ":", result[i][0], result[i][1], end=" | ")
            print(end="\r")

    print("\nch min  max")
    for k, v in result.items():
        print(k, v[0], v[1])

    if not no_save:
        try:
            with open(FILE, 'w') as f:
                json.dump(result, f)
        except Exception as err:
            print("Error while saving file", err)
        else:
            print("File saved")

    proc.terminate()


if __name__ == "__main__":
    q = Queue()
    uart_proc = Process(name='uart_reader', target=reader, args=(q,))
    uart_proc.start()

    calibration(uart_proc, q)
