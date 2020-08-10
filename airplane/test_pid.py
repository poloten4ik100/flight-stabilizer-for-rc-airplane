from pid import PID
import matplotlib.pyplot as plt


def test_pid():

    target = 30  # setpoint

    angle = 50  # error value

    N = 50

    a = PID(0.53, 0.00001, 0.12)

    x = []
    y = []

    for i in range(0, N):
        x.append(i)
        com = a.compute(target, angle)
        angle = angle + com
        y.append(angle)

    assert 29.5 <= y[len(y)-1] <= 30.5

    fig, ax = plt.subplots()
    ax.plot(x, y, "r-")
    ax.set_xlabel('time (s)')
    ax.set_ylabel('value (degree)')
    ax.grid()
    fig.savefig("pid.png")
    #plt.show()
