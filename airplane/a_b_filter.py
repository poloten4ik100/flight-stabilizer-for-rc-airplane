import time


class ABFilter:
    ''' Alpha - beta filter implementation '''

    def __init__(self, k: float = 0.01):
        self.__k: float = k
        self.__prev_value: float = 0.0
        self.__prev_time: float = time.time()

    def filter(self, gyro_val: float, accel_val: float) -> float:
        ''' filter val '''

        self.__prev_value = (1 - self.__k) * (self.__prev_value + ((time.time() - self.__prev_time) * gyro_val)) + self.__k * accel_val
        self.__prev_time = time.time()
        return self.__prev_value

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, val):
        self.__k = val
