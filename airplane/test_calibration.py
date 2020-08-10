import time
import random
from multiprocessing import Process, Queue

from calibration import calibration


def generator(queue: Queue, channels_count: int):
    while True:
        time.sleep(0.1)
        ch = random.randint(1, channels_count)
        value = random.randint(1345, 2432)
        queue.put((ch, value))


def test_calibration():
    queue: Queue = Queue()
    proc = Process(name='uart reader', target=generator, args=(queue, 6))
    proc.start()

    calibration(proc, queue, True)
