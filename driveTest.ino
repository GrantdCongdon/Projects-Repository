#include <Servo.h>
#include <stdio.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;
//
int rightMotorPWM = 1612;
int leftMotorPWM = 1408;
int correctionRate;
void setup() {
  rightMotor.attach(11);
  leftMotor.attach(9);
  pinMode(3, INPUT);
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(3), readEncoderRight, RISING);
  attachInterrupt(digitalPinToInterrupt(2), readEncoderLeft, FALLING);
  //Serial.begin(9600);
  
}

void loop() {
  //Makes the robot go until the robot travels 5 feet
  while (encoderCountRight <= 1031 && encoderCountLeft <= 1031) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    //Correction algorith
    
    if (encoderCountRight > encoderCountLeft) {
      int error = encoderCountRight - encoderCountLeft;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM += correction;
    }
    else if (encoderCountLeft > encoderCountRight) {
      int error = encoderCountLeft - encoderCountRight;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM += correction;
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }
    
  }
  stopMotors();
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1600;
  leftMotorPWM = 1400;
  delay(1000);
  exit(1);
}

void readEncoderRight() {
  encoderCountRight ++;
}
void readEncoderLeft() {
  encoderCountLeft++;
}
void moveBothMotors(int value1, int value2) {
  rightMotor.writeMicroseconds(value1);
  leftMotor.writeMicroseconds(value2);
}
void stopMotors() {
  rightMotor.writeMicroseconds(1500);
  leftMotor.writeMicroseconds(1500);
}
