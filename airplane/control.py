class Control:

    angle_min = 0
    angle_max = 180

    def __setStep(self):
        return self.__min + (self.__max - self.__min) * 0.7

    def __init__(self, pw_min=1500, pw_max=1500):
        """ New control element

            Args:
                pw_min: pulse width in microseconds, corresponding to the minimum control value
                pw_max: pulse width in microseconds, corresponding to the maximum control value
        """

        self.__min = pw_min
        self.__max = pw_max
        self.__threshold = self.__setStep()

    def setup(self, val):
        """ sets the value for the min and max pulse duration """

        if val < self.__min:
            self.__min = val
            self.__threshold = self.__setStep()
            return True
        elif val > self.__max:
            self.__max = val
            self.__threshold = self.__setStep()
            return True

    def degree(self, val: int) -> int:
        """ translate pulse duration to angle in degrees

            Returns:
                Int
        """

        if val > self.__max:
            return Control.angle_max
        elif val < self.__min:
            return Control.angle_min
        else:
            own = Control.angle_max - Control.angle_min
            ext = self.__max - self.__min
            return (val - self.__min) * own // ext + Control.angle_min

    def switch(self, val: int) -> bool:
        """ translate pulse duration to switch position

            Returns:
                True, if val more than 70% of (pw_max - pw_mix)
                None otherwise
        """

        if val >= self.__threshold:
            return True

    def variator(self, val: int, min_val: float, max_val: float) -> float:
        """ translate pulse duration to variator position (custom value)

            Args:
                val: input value
                min_val: min value of data
                max_val: max value of data

            Returns:
                Float
        """
        if val > self.__max:
            return max_val
        elif val < self.__min:
            return min_val
        else:
            own = max_val - min_val
            ext = self.__max - self.__min
            return (val - self.__min) * own / ext + min_val

    @property
    def max(self):
        return self.__max

    @property
    def min(self):
        return self.__min

    @max.setter
    def max(self, val):
        self.__max = val

    @min.setter
    def min(self, val):
        self.__min = val
