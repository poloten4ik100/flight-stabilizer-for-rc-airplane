class PID:
    ''' implementation of a proportional-integral-derivative (PID) Controller '''

    min_val = -90
    max_val = 90

    def __init__(self, Kp: float = 0, Ki: float = 0, Kd: float = 0):

        self.i_prev: float = 0.0
        self.error_prev: float = 0.0

        self.Kp: float = Kp
        self.Ki: float = Ki
        self.Kd: float = Kd

    def setK(self, Kp: float = 0, Ki: float = 0, Kd: float = 0):
        ''' Changes the pid controller coefficients '''

        self.i_prev: float = 0.0
        self.error_prev: float = 0.0

        self.Kp: float = Kp
        self.Ki: float = Ki
        self.Kd: float = Kd

    def compute(self, target: int, angle: int) -> float:
        ''' Returns measured process value '''

        error = target - angle

        k = self.Kp * error
        i = self.i_prev + self.Ki * error
        d = self.Kd * (error - self.error_prev)

        self.i_prev = i
        self.error_prev = error

        u = k + i + d

        if u < PID.min_val:
            return PID.min_val
        elif u > PID.max_val:
            return PID.max_val
        else:
            return u
