#include <Servo.h>
#include <stdio.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;
//Set the PWM frequency for each motor
int rightMotorPWM = 1500;
int leftMotorPWM = 1500;
int loopLap = 0;
void setup() {
  //Attach motors to pins
  rightMotor.attach(11);
  leftMotor.attach(9);
  //Setup pins used for encoders
  pinMode(3, INPUT);
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(3), readEncoderRight, RISING);
  attachInterrupt(digitalPinToInterrupt(2), readEncoderLeft, FALLING);
  //Begin serial communication
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  moveBothMotors(rightMotorPWM, leftMotorPWM);
  delay(1000);
  while (true) {
    delay(1000);
    if (encoderCountRight==0) {
      break;
    }
    else {
      while (encoderCountRight!=0) {
        if (encoderCountRight >= 1550) {
          loopLap = 1;
        }
        if (loopLap==0) {
          rightMotorPWM+=1;
        }
        else {
          rightMotorPWM-=1;
        }
        encoderCountRight = 0;
        moveBothMotors(rightMotorPWM, leftMotorPWM);
        delay(1000);
      }
    }
    encoderCountRight = 0;
  }
  Serial.println("Right Motor:");
  Serial.println(rightMotorPWM);
  encoderCountLeft = 0;
  delay(1000);
  while (true) {
    delay(1000);
    if (encoderCountLeft==0) {
      break;
    }
    else {
      while (encoderCountLeft!=0) {
        if (encoderCountLeft >= 1550) {
          loopLap = 1;
        }
        if (loopLap==0) {
          leftMotorPWM+=1;
        }
        else {
          leftMotorPWM-=1;
        }
        encoderCountLeft=0;
        moveBothMotors(rightMotorPWM, leftMotorPWM);
        delay(1000);
      }
    }
    encoderCountLeft=0;
  }
  Serial.println("Left Motor:");
  Serial.println(leftMotorPWM);
  stopMotors();

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
