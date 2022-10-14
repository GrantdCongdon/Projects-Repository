#include <AFMotor.h>
AF_DCMotor rightMotor(1, MOTOR12_64KHZ);
AF_DCMotor leftMotor(2, MOTOR12_64KHZ);void setup() {
  // put your setup code here, to run once:
  rightMotor.setSpeed(150);
  leftMotor.setSpeed(150);
  pinMode(2, OUTPUT);
  pinMode(A0, OUTPUT);
  digitalWrite(2, HIGH);
  digitalWrite(A0, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  rightMotor.run(FORWARD);
  leftMotor.run(FORWARD);
  delay(1000);
  rightMotor.run(RELEASE);
  leftMotor.run(RELEASE);
  delay(1000);
}
