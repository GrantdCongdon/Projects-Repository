#include <Servo.h>
#include <stdio.h>
Servo motor;
const int midpoint = 1400;
const int conveyorPWM = 1250;
void setup() {
  motor.attach(2);
  Serial.begin(9600);
  stopMotor();
  Serial.println("Start");
}

void loop() {
  moveMotor(conveyorPWM);
}
void moveMotor(int value) {
  motor.writeMicroseconds(value);
}
void stopMotor() {
  motor.writeMicroseconds(midpoint);
}
void countDown(int iterations, int t) {
  Serial.print("Starting in ");
  for (int i=0; i < iterations; i++) {
    Serial.println(iterations-i);
    delay(t*1000);
  }
  Serial.println("Start");
}
