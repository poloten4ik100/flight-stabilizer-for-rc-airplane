import serial


def reader(queue):

    ser = serial.Serial('/dev/ttyAMA0', 115200)

    while True:

        line = ser.readline()

        if line != '':
            ln = line.decode("ascii").split()
            queue.put((int(ln[0]), int(ln[1])))
