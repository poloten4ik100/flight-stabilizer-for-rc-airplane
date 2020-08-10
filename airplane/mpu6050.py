import smbus
import math
import time


class MPU6050:
    PWR_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C
    INT_ENABLE = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H = 0x43
    GYRO_YOUT_H = 0x45
    GYRO_ZOUT_H = 0x47
    Device_Addr = 0x68  # MPU6050 device address

    def __init__(self):
        self.bus = smbus.SMBus(1)

        # Sample Rate Divider register
        # Sample Rate = Gyroscope Output Rate / (1 + SMPLRT_DIV)
        # where Gyroscope Output Rate = 8kHz when the DLPF is disabled (DLPF_CFG = 0 or 7), and 1kHz
        # when the DLPF is enabled (in CONFIG register).
        # I used 1kHz
        self.bus.write_byte_data(MPU6050.Device_Addr, MPU6050.SMPLRT_DIV, 7)

        # Power management register
        # I used internal 8MHz oscillator
        self.bus.write_byte_data(MPU6050.Device_Addr, MPU6050.PWR_MGMT_1, 0)

        # Configuration register
        # No external signal for synchronization, filtering is set to 0
        self.bus.write_byte_data(MPU6050.Device_Addr, MPU6050.CONFIG, 0)

        # Gyro configuration register
        # No self-test, FS_SEL Full Scale Range (bits 3-4)
        # dec 24 in bin: 11000 (FS_SEL = 3 (11) +/- 2000 degrees/s)
        #    0 (00) +/- 250 degrees/s
        #    1 (01) +/- 500 degrees/s
        #    2 (10) +/- 1000 degrees/s
        #    3 (11) +/- 2000 degrees/s
        self.bus.write_byte_data(MPU6050.Device_Addr, MPU6050.GYRO_CONFIG, 24)

        # Accelerometer configuration register
        # No self-test, AFS_SEL Full Scale Range (bits 3-4)
        # dec 24 in bin: 11000 (AFS_SEL = 3 (11) +/- 16g)
        # 0 (00) +/- 2g
        # 1 (01) +/- 4g
        # 2 (10) +/- 8g
        # 3 (11) +/- 16g
        self.bus.write_byte_data(MPU6050.Device_Addr, MPU6050.ACCEL_CONFIG, 24)

        self.time = time.time()
        self.filter_roll = 0.0
        self.filter_pitch = 0.0
        self.g_x = 0
        self.g_y = 0

    def get_data(self):
        ''' get angular velocity from gyro and acceleration from mpu6050 '''

        try:
            # Read Accelerometer raw value
            accel_raw_x = self._read_raw_data(MPU6050.ACCEL_XOUT_H)
            accel_raw_y = self._read_raw_data(MPU6050.ACCEL_YOUT_H)
            accel_raw_z = self._read_raw_data(MPU6050.ACCEL_ZOUT_H)

            # Read Gyroscope raw value
            gyro_raw_x = self._read_raw_data(MPU6050.GYRO_XOUT_H)
            gyro_raw_y = self._read_raw_data(MPU6050.GYRO_YOUT_H)
            gyro_raw_z = self._read_raw_data(MPU6050.GYRO_ZOUT_H)
        except Exception:
            return (0, 0)

        # Full scale range +/- 16g (2048 LSB/g)
        accel_x = accel_raw_x / 2048.0
        accel_y = accel_raw_y / 2048.0
        accel_z = accel_raw_z / 2048.0

        # Full scale range +/- 2000 degrees/s - 16.4 LSB/degrees/s
        gyro_x = gyro_raw_x / 16.4
        gyro_y = gyro_raw_y / 16.4
        gyro_z = gyro_raw_z / 16.4

        return gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z

    def _read_raw_data(self, addr):
        high = self.bus.read_byte_data(MPU6050.Device_Addr, addr)
        low = self.bus.read_byte_data(MPU6050.Device_Addr, addr+1)

        # Concatenate higher and lower value
        value = ((high << 8) | low)

        # Get signed value
        if(value > 32768):
            value = value - 65536
        return value
