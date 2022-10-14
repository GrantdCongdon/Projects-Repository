#include <Servo.h>
#include <stdio.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;
//
int rightMotorPWM = 1250;
int leftMotorPWM = 1750;
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
      rightMotorPWM+=1;
      if (rightMotorPWM >= 1300) {
        rightMotorPWM-=2;
      }
    }
    else if (encoderCountLeft > encoderCountRight) {
      leftMotorPWM-=1;
      if (leftMotorPWM <= 1700) {
        leftMotorPWM+=2;
      }
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }
    
  }
  stopMotors();
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM=1300;
  leftMotorPWM=1800;
  while (encoderCountRight <= 486 && encoderCountLeft <= 742) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    /*Serial.println(encoderCountRight);
    Serial.println(encoderCountLeft);*/
  }
  stopMotors();
  delay(1000);
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1250;
  leftMotorPWM = 1750;
  delay(1000);
  return 0;
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
