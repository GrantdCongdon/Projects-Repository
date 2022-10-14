#include <Servo.h>
#include <stdio.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
SoftwareSerial mySerial(7, 6);
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;

// Variables for pwm signal for both motors
int rightMotorPWM = 1750;
int leftMotorPWM = 1250;
//Rate at which the robot will correct itself
int correctionRate = 0.5;
//Cancels if correction is going overboard
int cancelRight = 1;
int cancelLeft = 1;
//Encoder Count for 10 feet with new robot
int rightMotorTenFeet = 1547;
int leftMotorTenFeet = 1547;
//Encoder Count for 90 degree turn with new robot
int outboardWheelTurn = 518;
int inboardWheelTurn = 939;
//Correction failsafe for right and left motors
int rightMotorFailsafe = 1800;
int leftMotorFailsafe = 1200;
void setup() {
  //Attach motors to pwm pins
  rightMotor.attach(11);
  leftMotor.attach(9);
  //Sets up the interrupt pins
  pinMode(3, INPUT);
  pinMode(2, INPUT);
  //One pin triggers whenever the encoder signal is rising from low to high and the other one triggers vice versa
  attachInterrupt(digitalPinToInterrupt(3), readEncoderRight, RISING);
  attachInterrupt(digitalPinToInterrupt(2), readEncoderLeft, FALLING);
}
void loop() {
  delay(3000);
  //Start loop that makes the robot go 10 feet forward
  while (encoderCountRight <= rightMotorTenFeet && encoderCountLeft <= leftMotorTenFeet) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //Correction algorith
    if (encoderCountRight > encoderCountLeft) {
      if (leftMotorPWM < leftMotorFailsafe) {
        cancelLeft = 0;
      }
      else {
        cancelLeft = 1;
      }
      int error = encoderCountRight - encoderCountLeft;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction * cancelLeft;
      
    }
    else if (encoderCountLeft > encoderCountRight) {
      if (rightMotorPWM > rightMotorFailsafe) {
        cancelRight = 0;
      }
      else {
        cancelRight = 1;
      }
      int error = encoderCountLeft - encoderCountRight;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction * cancelRight;
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }
    
  }
  //Calls the function that stops both motors
  stopMotors();
  delay(500);
  //Resets the encoders for turning
  encoderCountRight = 0;
  encoderCountLeft = 0;
  //Sets PWM signals that the motors with use for turning
  rightMotorPWM=1300;
  leftMotorPWM=1800;
  //Runs both motors until each motor runs their amount around the circumference
  while (encoderCountRight <= inboardWheelTurn && encoderCountLeft <= outboardWheelTurn) {
    moveBothMotors(rightMotorPWM, leftMotorPWM-150);
  }
  //Stops motors
  stopMotors();
  delay(500);
  //Resets the encoders and PWM signals for another run through so that the robot can go through a square
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1600;
  leftMotorPWM = 1400;
  while (encoderCountRight <= rightMotorTenFeet && encoderCountLeft <= leftMotorTenFeet) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //Correction algorith
    if (encoderCountRight > encoderCountLeft) {
      if (leftMotorPWM < leftMotorFailsafe) {
        cancelLeft = 0;
      }
      else {
        cancelLeft = 1;
      }
      int error = encoderCountRight - encoderCountLeft;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction * cancelLeft;
      
    }
    else if (encoderCountLeft > encoderCountRight) {
      if (rightMotorPWM > rightMotorFailsafe) {
        cancelRight = 0;
      }
      else {
        cancelRight = 1;
      }
      int error = encoderCountLeft - encoderCountRight;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction * cancelRight;
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }  
  }
  //Calls the function that stops both motors
  stopMotors();
  delay(500);
  //Resets the encoders for turning
  encoderCountRight = 0;
  encoderCountLeft = 0;
  //Sets PWM signals that the motors with use for turning
  rightMotorPWM=1300;
  leftMotorPWM=1800;
  //Runs both motors until each motor runs their amount around the circumference
  while (encoderCountRight <= inboardWheelTurn && encoderCountLeft <= outboardWheelTurn) {
    moveBothMotors(rightMotorPWM, leftMotorPWM-150);
  }
  //Stops motors
  stopMotors();
  delay(500);
  //Resets the encoders and PWM signals for another run through so that the robot can go through a square
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1600;
  leftMotorPWM = 1400;
  while (encoderCountRight <= rightMotorTenFeet && encoderCountLeft <= leftMotorTenFeet) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //Correction algorith
    if (encoderCountRight > encoderCountLeft) {
      if (leftMotorPWM < leftMotorFailsafe) {
        cancelLeft = 0;
      }
      else {
        cancelLeft = 1;
      }
      int error = encoderCountRight - encoderCountLeft;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction * cancelLeft;
      
    }
    else if (encoderCountLeft > encoderCountRight) {
      if (rightMotorPWM > rightMotorFailsafe) {
        cancelRight = 0;
      }
      else {
        cancelRight = 1;
      }
      int error = encoderCountLeft - encoderCountRight;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction * cancelRight;
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }  
  }
  //Calls the function that stops both motors
  stopMotors();
  delay(500);
  //Resets the encoders for turning
  encoderCountRight = 0;
  encoderCountLeft = 0;
  //Sets PWM signals that the motors with use for turning
  rightMotorPWM=1300;
  leftMotorPWM=1800;
  //Runs both motors until each motor runs their amount around the circumference
  while (encoderCountRight <= inboardWheelTurn && encoderCountLeft <= outboardWheelTurn) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
  }
  //Stops motors
  stopMotors();
  delay(500);
  //Resets the encoders and PWM signals for another run through so that the robot can go through a square
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1600;
  leftMotorPWM = 1400;
  while (encoderCountRight <= rightMotorTenFeet && encoderCountLeft <= leftMotorTenFeet) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //Correction algorith
    if (encoderCountRight > encoderCountLeft) {
      if (leftMotorPWM < leftMotorFailsafe) {
        cancelLeft = 0;
      }
      else {
        cancelLeft = 1;
      }
      int error = encoderCountRight - encoderCountLeft;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction * cancelLeft;
      
    }
    else if (encoderCountLeft > encoderCountRight) {
      if (rightMotorPWM > rightMotorFailsafe) {
        cancelRight = 0;
      }
      else {
        cancelRight = 1;
      }
      int error = encoderCountLeft - encoderCountRight;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction * cancelRight;
    }
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }  
  }
  stopMotors();
  //Makes sure than the program doesn't run again
  rightMotorPWM = 1000;
  leftMotorPWM = 1000;
  //Tries to exit the program
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
  return 0;
}
void stopMotors() {
  rightMotor.writeMicroseconds(1500);
  leftMotor.writeMicroseconds(1500);
  return 0;
}

void accelerateBothMotors(int rightValue, int leftValue) {
  if (rightValue>1500 && leftValue<1500) {
    for (int i = 1500; i < rightValue; i+=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e > leftValue; e-=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue>1500 && leftValue>1500) {
    for (int i = 1500; i < rightValue; i+=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e < 1500; e+=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue<1500 && leftValue>1500) {
    for (int i = 1500; i > rightValue; i-=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e < 1500; e+=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue<1500 && leftValue<1500) {
    for (int i = 0; i > rightValue; i-=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 0; e > leftValue; e-=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  return 0;
}
