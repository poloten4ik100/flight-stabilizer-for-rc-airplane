## Stabilizer for rc airplane
---
two-axis flight stabilizer for radio-controlled airplane.
```
                                                        -> accel&gyro (angle from mpu6050, roll and pitch) 
rc receiver (pwm) --> arduino >-uart-> raspberry pi <-i2c
                                                        -> servo control (Adafruit PCA9685)
```

### Setup & Configuration

1. Upload the sketch into arduino

2. Connect the remote control receiver to arduino

ATmega328 pin | Uno pin | Nano pin | Chan number | Role
--- | --- | --- | --- | ---
PB1 | 9 | D9 | **1** | ROLL
PB2 | 10 | D10 | **2** | PITCH
PB3 | 11 | D11 | **3** | VARIATOR (alpha beta filter ratio)
PB4 | 12 | D12 | **4** | STABILIZER SWITCH (On/Off stabilizer)

3. Connect arduino to raspberry pi via uart

4. Connect mpu6050 to raspberry pi via i2c

5. Connect Adafruit PCA9685 to raspberry pi via i2c

6. Connect servos to Adafruit PCA9685

You can edit default constants in airplane.py: CHAN_ROLL, CHAN_PITCH, CHAN_VARIATOR, CHAN_STABILIZER_SWITCH

### Launch

```
python3 airplane.py
```

### Calibration

It is recommended to calibrate the PWM data from the rc receiver before the first start

```
python3 calibration.py
```

While running the script, move the necessary control levers of the remote control from the lowest to the highest position to measure the minimum and maximum time of the PWM pulse length in microseconds

Сalibration takes 30 seconds

These values will be shown on the screen from 0 to 6 channel

At the end, the results will be saved to a file calibration.json
