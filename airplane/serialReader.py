import serial
import sys

def reader(queue):

    ser = serial.Serial('/dev/ttyAMA0', 115200)

    error_counter = 1

    while True:
        try:
            line = ser.readline()

            if line != '':
                ln = line.decode("ascii").split()
                queue.put((int(ln[0]), int(ln[1])))
        except Exception as error:
            print("uart read error", error_counter, error)
            error_counter += 1
            if error_counter > 5:
                sys.exit("uart read error:", error)
        
