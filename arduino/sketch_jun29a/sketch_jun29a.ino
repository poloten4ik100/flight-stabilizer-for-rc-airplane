#include "PinChangeInterrupt.h"

#define PIN_4 4 // PB4 (12)
#define PIN_3 3 // PB3 (11)
#define PIN_2 2 // PB2 (10)
#define PIN_1 1 // PB1 (9)

int prev_time_1 = 0;
int prev_time_2 = 0;
int prev_time_3 = 0;
int prev_time_4 = 0;

int pwm_value_1 = 0;

void rising_1()
{
  attachPinChangeInterrupt(PIN_1, &falling_1, FALLING);
  prev_time_1 = micros();
} 

void falling_1() {
  attachPinChangeInterrupt(PIN_1, &rising_1, RISING);
  Serial.print(PIN_1);
  Serial.print(" ");
  int tmp = micros()-prev_time_1;
  Serial.println(tmp);
}

void rising_2()
{
  attachPinChangeInterrupt(PIN_2, &falling_2, FALLING);
  prev_time_2 = micros();
} 
void falling_2() {
  attachPinChangeInterrupt(PIN_2, &rising_2, RISING);
  int new_pwm = micros()-prev_time_2;
  Serial.print(PIN_2);
  Serial.print(" ");
  Serial.println(new_pwm);
}

void rising_3()
{
  attachPinChangeInterrupt(PIN_3, &falling_3, FALLING);
  prev_time_3 = micros();
} 
void falling_3() {
  attachPinChangeInterrupt(PIN_3, &rising_3, RISING);
  int new_pwm = micros()-prev_time_3;
  Serial.print(PIN_3);
  Serial.print(" ");
  Serial.println(new_pwm);
}

void rising_4()
{
  attachPinChangeInterrupt(PIN_4, &falling_4, FALLING);
  prev_time_4 = micros();
} 
void falling_4() {
  attachPinChangeInterrupt(PIN_4, &rising_4, RISING);
  int new_pwm = micros()-prev_time_4;
  Serial.print(PIN_4);
  Serial.print(" ");
  Serial.println(new_pwm);
}

void setup() {
  Serial.begin(115200);
  attachPinChangeInterrupt(PIN_1, &rising_1, RISING);
  attachPinChangeInterrupt(PIN_2, &rising_2, RISING);
  attachPinChangeInterrupt(PIN_3, &rising_3, RISING);
  attachPinChangeInterrupt(PIN_4, &rising_4, RISING);
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
