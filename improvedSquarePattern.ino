 //Import necessary libraries
#include <Servo.h>
#include <stdio.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Wire.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;
//setup initial pwm speeds for both motors. 1500 being the midpoint
int rightMotorPWM = 1725;
int leftMotorPWM = 1350;
//set correction rate proportionality to speed or slow corrections
float correctionRate = 0.5;
//Almost perfect correction rate is 0.7!
//cancel corrections if necessary
int cancelLeft = 1;
int cancelRight = 1;
//define pi
double pi = 3.1415926535;
//declare compass
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);
//Constant for centering motors
float regresarConstant = 0.925;
//Turn count for both motors
int inboardWheelPulses = 400;
int outboardWheelPulses = 450;
//Midpoint
int rightMotorMidpoint = 1507;
int leftMotorMidpoint = 1508;
//Scalepoint for testing
float scalepoint = 2;
//Offset correction line
int offset = 3;
//for a fix of the correction algorith
float highpointSpecial;
//right motor PWM max and left motor minimium
int rightMotorMax = 1900;
int leftMotorMin = 1200;
void setup() {
  //attach motors to pins
  rightMotor.attach(11);
  leftMotor.attach(9);
  //set up pins for the encoders
  pinMode(3, INPUT);
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(3), readEncoderRight, RISING);
  attachInterrupt(digitalPinToInterrupt(2), readEncoderLeft, FALLING);
  //check to see if the digital compass is working
  if(!mag.begin())
  {
    //Stop prgram if there is compass problem
    while(1);
  }
  //Serial.begin(9600);
  //stop both motors to stop 'drifting' at the start of the program
  moveBothMotors(rightMotorMidpoint, leftMotorMidpoint);
  //set up for initial straightaway
  rightMotorPWM = 1725;
  leftMotorPWM = 1350;
}

void loop() {
  // put your main code here, to run repeatedly:
  //wait 5 seconds to get everything set up
  delay(5000);
  //get compass heading for the base reading used to compare to future readings
  float baseHeading = getCompassReading();
  float highpoint = baseHeading + offset;
  float lowpoint = baseHeading - offset;
  //inverse if greater than 180 to make correction algorith work
  if (baseHeading > 180 && highpoint > 360) {
    baseHeading = (360-baseHeading)*-1;
    highpointSpecial = highpoint - 360;
  }
  else {
    baseHeading = baseHeading;
  }
  //start loop that makes the robot go about 15 feet
  while (encoderCountRight <= 1000*scalepoint && encoderCountLeft <= 1000*scalepoint) {
    //get another compass heading
    float firstHeading = getCompassReading();
    //inverse if needed to make correction algorith work
    if (firstHeading > 180 && highpoint > 360) {
      firstHeading = (360-firstHeading) * -1;
    }
    else if (firstHeading > 180 && lowpoint < 0) {
      firstHeading = (360-firstHeading) * -1;
    }
    else {
      firstHeading = firstHeading;
    }
    //start the robot
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //correction algorith
    //check to see if teh robot is drifting to the right
    if (firstHeading > highpointSpecial) {
      cancelLeft = 1;
      //calculate the amount of error that exists
      int error = firstHeading - baseHeading;
      //applifiy correction amount based on error and set correction constant
      int correction = error/correctionRate;
      //change the speed of the motor based on the correction amount previously calculated
      rightMotorPWM = rightMotorPWM + correction;
      //do you have to have times cancelLeft if cancelLeft is just 1? -Bryn
      //make sure robot doesn't go too fast by applying a constant that will slow the robot down if the correction algorith goes crazy
      if (encoderCountRight > 300 && leftMotorPWM < leftMotorMin) {
        rightMotorPWM = rightMotorPWM * regresarConstant;
      }
    }
    //do the same thing on the just if the robot is going too much to the left
    else if (firstHeading < lowpoint) {
      cancelRight = 1;
      int error = baseHeading - firstHeading;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction;
      if (encoderCountLeft > 300 && rightMotorPWM > rightMotorMax) {
        leftMotorPWM = leftMotorPWM * ((1-regresarConstant)+1);
      }
    }
    //if the robot is going in the general straight direction then keep everything the same
    else {
      rightMotorPWM = 1725;
      leftMotorPWM = 1350;
      
    }
  }
  //give the robot time to think and go a little bit farther to be safe
  delay(100);
  //reset encoders so that the turn works and the proccessor has smaller numbers to count to as well as simplifing the maths
  encoderCountRight=0;
  encoderCountLeft=0;
  //set up motor speeds for the turn
  rightMotorPWM = 1900;
  leftMotorPWM = 1400;
  //drive robot unitl the encoders both reach the distance they need to in order to complete a 90 degree turn
  while (encoderCountLeft <= inboardWheelPulses && encoderCountRight <= outboardWheelPulses) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    //stops the motors so the robot doesn't overturn
    if (encoderCountRight >= outboardWheelPulses) {
      rightMotor.writeMicroseconds(rightMotorMidpoint);
    }
    else if (encoderCountLeft >= inboardWheelPulses) {
      leftMotor.writeMicroseconds(leftMotorMidpoint);
    }
  }
  //resets encoders for the straightaway for the same reasons as before
  encoderCountRight=0;
  encoderCountLeft=0;
  //starts the motors going forward
  moveBothMotors(1725, 1350);
  delay(50);
  //sets variables for the straightaway
  rightMotorPWM = 1725;
  leftMotorPWM = 1350;
  //Reset baseHeading reading because perfect system doesnt seem to work to well
  baseHeading = getCompassReading();
  //resets the highpoint and lowpoint readings based on new baseheading
  highpoint = baseHeading + offset;
  lowpoint = baseHeading - offset;
  //baseheading and highpoint manipulation in order to get the correction algorith to work
  if (baseHeading > 180 && highpoint > 360) {
    baseHeading = (360-baseHeading)*-1;
    highpointSpecial = highpoint - 360;;
  }
  else {
    baseHeading = baseHeading;
  }
  //robot's seocnd starightaway
  while (encoderCountRight <= 750*scalepoint && encoderCountLeft <= 750*scalepoint) {
    //get another compass heading
    float firstHeading = getCompassReading();
    //inverse if needed to make correction algorith work
    if (firstHeading > 180 && highpoint > 360) {
      firstHeading = (360-firstHeading) * -1;
    }
    else if (firstHeading > 180 && lowpoint < 0) {
      firstHeading = (360-firstHeading) * -1;
    }
    else {
      firstHeading = firstHeading;
    }
    //start the robot
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //correction algorith
    if (firstHeading > highpointSpecial) {
      cancelLeft = 1;
      int error = firstHeading - baseHeading;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM + correction * cancelLeft;
      if (encoderCountRight > 300 && leftMotorPWM < leftMotorMin) {
        leftMotorPWM = leftMotorPWM * ((1-regresarConstant)+1);
      }
    }
    else if (firstHeading < lowpoint) {
      cancelRight = 1;
      int error = baseHeading - lowpoint;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM - correction * cancelRight;
      if (encoderCountLeft > 300 && rightMotorPWM > rightMotorMax) {
        rightMotorPWM = rightMotorPWM * regresarConstant;
      }
    }
    else {
      rightMotorPWM = 1725;
      leftMotorPWM = 1350;
      
    }
  }
  delay(100);
  encoderCountRight=0;
  encoderCountLeft=0;
  rightMotorPWM = 1900;
  leftMotorPWM = 1400;
  while (encoderCountLeft <= inboardWheelPulses && encoderCountRight <= outboardWheelPulses) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    if (encoderCountRight >= outboardWheelPulses) {
      rightMotor.writeMicroseconds(rightMotorMidpoint);
    }
    else if (encoderCountLeft >= inboardWheelPulses) {
      leftMotor.writeMicroseconds(leftMotorMidpoint);
    }
  }
  encoderCountRight=0;
  encoderCountLeft=0;
  moveBothMotors(1725, 1350);
  delay(50);
  rightMotorPWM = 1725;
  leftMotorPWM = 1350;
  
  baseHeading = getCompassReading();
  
  highpoint = baseHeading + offset;
  lowpoint = baseHeading - offset;
  
  if (baseHeading > 180 && highpoint > 360) {
    baseHeading = (360-baseHeading)*-1;
    highpointSpecial = highpoint - 360;
  }
  else {
    baseHeading = baseHeading;
  }
  
  while (encoderCountRight <= 2000*scalepoint && encoderCountLeft <= 2000*scalepoint) {
    //get another compass heading
    float firstHeading = getCompassReading();
    //inverse if needed to make correction algorith work
    if (firstHeading > 180 && highpoint > 360) {
      firstHeading = (360-firstHeading) * -1;
    }
    else if (firstHeading > 180 && lowpoint < 0) {
      firstHeading = (360-firstHeading) * -1;
    }
    else {
      firstHeading = firstHeading;
    }
    //start the robot
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(100);
    //correction algorith
    if (firstHeading > highpointSpecial) {
      cancelLeft = 1;
      int error = firstHeading - baseHeading;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction;
      //do you have to have times cancelLeft if cancelLeft is just 1? -Bryn
      if (encoderCountRight > 300 && rightMotorPWM > rightMotorMax) {
        rightMotorPWM = rightMotorPWM * regresarConstant;
      }
    }
    else if (firstHeading < lowpoint) {
      cancelRight = 1;
      int error = baseHeading - firstHeading;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction;
      if (encoderCountLeft > 300 && leftMotorPWM < leftMotorMin) {
        leftMotorPWM = leftMotorPWM * ((1-regresarConstant)+1);
      }
    }
    else {
      rightMotorPWM = 1725;
      leftMotorPWM = 1350;
    }
  }
  delay(100);
  encoderCountRight=0;
  encoderCountLeft=0;
  rightMotorPWM = 1900;
  leftMotorPWM = 1400;
  while (encoderCountLeft <= inboardWheelPulses && encoderCountRight <= outboardWheelPulses) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    if (encoderCountRight >= outboardWheelPulses) {
      rightMotor.writeMicroseconds(rightMotorMidpoint);
    }
    else if (encoderCountLeft >= inboardWheelPulses) {
      leftMotor.writeMicroseconds(leftMotorMidpoint);
    }
  }
  encoderCountRight=0;
  encoderCountLeft=0;
  moveBothMotors(1725, 1350);
  delay(50);
  rightMotorPWM = 1725;
  leftMotorPWM = 1350;
  encoderCountRight = 0;
  encoderCountLeft = 0;
  baseHeading = getCompassReading();
  highpoint = baseHeading + offset;
  lowpoint = baseHeading - offset;
  if (baseHeading > 180 && highpoint > 360) {
    baseHeading = (360-baseHeading)*-1;
    highpointSpecial = 360 - highpoint;
  }
  else {
    baseHeading = baseHeading;
  }
  while (encoderCountRight <= 750*scalepoint && encoderCountLeft <= 750*scalepoint) {
    //get another compass heading
    float firstHeading = getCompassReading();
    //inverse if needed to make correction algorith work
    if (firstHeading > 180 && highpoint > 360) {
      firstHeading = (360-firstHeading) * -1;
    }
    else if (firstHeading > 180 && lowpoint < 0) {
      firstHeading = (360-firstHeading) * -1;
    }
    else {
      firstHeading = firstHeading;
    }
    //start the robot
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //correction algorith
    if (firstHeading > highpointSpecial) {
      cancelLeft = 1;
      int error = firstHeading - baseHeading;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM + correction * cancelLeft;
      if (encoderCountRight > 300 && leftMotorPWM < leftMotorMin) {
        leftMotorPWM = leftMotorPWM * ((1-regresarConstant)+1);
      }
    }
    else if (firstHeading < lowpoint) {
      cancelRight = 1;
      int error = baseHeading - firstHeading;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM - correction * cancelRight;
      if (encoderCountLeft > 300 && rightMotorPWM > rightMotorMax) {
        rightMotorPWM = rightMotorPWM * regresarConstant;
      }
    }
    else {
      rightMotorPWM = 1725;
      leftMotorPWM = 1350;
      
    }
  }
  moveBothMotors(1725, 1350);
  delay(250);
  encoderCountRight=0;
  encoderCountLeft=0;
  rightMotorPWM = 1900;
  leftMotorPWM = 1400;
  while (encoderCountLeft <= inboardWheelPulses && encoderCountRight <= outboardWheelPulses) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    if (encoderCountRight >= outboardWheelPulses) {
      rightMotor.writeMicroseconds(rightMotorMidpoint);
    }
    else if (encoderCountLeft >= inboardWheelPulses) {
      leftMotor.writeMicroseconds(leftMotorMidpoint);
    }
  }
  encoderCountRight=0;
  encoderCountLeft=0;
  moveBothMotors(1725, 1350);
  delay(50);
  rightMotorPWM = 1725;
  leftMotorPWM = 1350;
  encoderCountRight = 0;
  encoderCountLeft = 0;
  baseHeading = getCompassReading();
  highpoint = baseHeading + offset;
  lowpoint = baseHeading - offset;
  if (baseHeading > 180 && highpoint > 360) {
    baseHeading = (360-baseHeading)*-1;
    highpointSpecial = 360 - highpoint;
  }
  else {
    baseHeading = baseHeading;
  }
  //last straightaway and turn because you start in the middle of a rectangle not on one of the corners
  while (encoderCountRight <= 1000*scalepoint && encoderCountLeft <= 1000*scalepoint) {
    //get another compass heading
    float firstHeading = getCompassReading();
    //inverse if needed to make correction algorith work
    if (firstHeading > 180 && highpoint > 360) {
      firstHeading = (360-firstHeading) * -1;
    }
    else if (firstHeading > 180 && lowpoint < 0) {
      firstHeading = (360-firstHeading) * -1;
    }
    else {
      firstHeading = firstHeading;
    }
    //start the robot
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    delay(250);
    //correction algorith
    if (firstHeading > highpointSpecial) {
      cancelLeft = 1;
      int error = firstHeading - baseHeading;
      int correction = error/correctionRate;
      rightMotorPWM = rightMotorPWM + correction;
      //do you have to have times cancelLeft if cancelLeft is just 1? -Bryn
      if (encoderCountRight > 300 && leftMotorPWM < leftMotorMin) {
        rightMotorPWM = rightMotorPWM * regresarConstant;
      }
    }
    else if (firstHeading < lowpoint) {
      cancelRight = 1;
      int error = baseHeading - firstHeading;
      int correction = error/correctionRate;
      leftMotorPWM = leftMotorPWM - correction;
      if (encoderCountLeft > 300 && rightMotorPWM > rightMotorMax) {
        leftMotorPWM = leftMotorPWM * ((1-regresarConstant)+1);
      }
    }
    else {
      rightMotorPWM = 1725;
      leftMotorPWM = 1350;
    }
  }
  delay(100);
  //the rest of the program is just to get the robot to stop and is completely necessary sadly.
  encoderCountRight = 5000;
  encoderCountLeft = 5000;
  moveBothMotors(rightMotorMidpoint, leftMotorMidpoint);
  for (int i = 0; i < 500; i++) {
    stopMotors();
  }
  encoderCountRight=5000;
  encoderCountLeft=5000;
  rightMotorPWM=rightMotorMidpoint;
  leftMotorPWM=leftMotorMidpoint;
  moveBothMotors(rightMotorPWM, leftMotorPWM);
  moveBothMotors(rightMotorMidpoint, leftMotorMidpoint);
  exit(1);
}
//function that runs constantly that counts the right encoder
void readEncoderRight() {
  encoderCountRight++;
}
//same function just counts the left encoder
void readEncoderLeft() {
  encoderCountLeft++;
}
//function for moving both motors
void moveBothMotors(int value1, int value2) {
  rightMotor.writeMicroseconds(value1);
  leftMotor.writeMicroseconds(value2);
}
//stops both motors
void stopMotors() {
  rightMotor.writeMicroseconds(rightMotorMidpoint);
  leftMotor.writeMicroseconds(leftMotorMidpoint);
}
//relatively new function that gets compass readings and really simplifies the whole process
float getCompassReading() {
  sensors_event_t event;
  mag.getEvent(&event);
  float heading = (atan2(event.magnetic.y,event.magnetic.x) * 180) / pi;
  while (heading == 0.0) {
    heading = (atan2(event.magnetic.y,event.magnetic.x) * 180) / pi;
    if (heading < 0) {
      heading = 360 + heading;
    }
  }
  return heading;
}
