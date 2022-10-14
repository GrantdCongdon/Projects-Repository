#include <AFMotor.h>
AF_DCMotor rightMotor(1, MOTOR12_64KHZ);
AF_DCMotor leftMotor(2, MOTOR12_64KHZ);
void setup() {
  // put your setup code here, to run once:
  //Serial.begin(9600);
  rightMotor.setSpeed(150);
  leftMotor.setSpeed(150);
}

void loop() {
  // put your main code here, to run repeatedly:
  rightMotor.run(FORWARD);
  delay(1000);
  rightMotor.run(BACKWARD);
  delay(1000);
  rightMotor.run(RELEASE);
  delay(1000);
  leftMotor.run(FORWARD);
  delay(1000);
  leftMotor.run(BACKWARD);
  delay(1000);
  leftMotor.run(RELEASE);
  delay(1000);
}
