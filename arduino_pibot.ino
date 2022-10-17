//import libraries
#include <Servo.h>
#include <stdio.h>
//make servos
Servo rightservo;
Servo leftservo;
Servo armservo;
//set varaibles for program
int value;
int varCode;
int getRight;
int getLeft;
int getArm;
int loopLap;
//run this code once
void setup() {
  rightservo.attach(9); //rightservo set to pin 9
  leftservo.attach(10); //leftservo set to pin 10
  armservo.attach(5); //armservo set to pin 5
  Serial.begin(9600); //start serial communication at 9600 buad
}
//loop this code
void loop() {
  //run while serial communication is in place
  while (Serial.available()) {
    if (loopLap == 0) {
      //reads 1 character at a time and the first character determines whcih motor to move
      varCode = Serial.read();
      //Serial.println(varCode);
    }
    //ascii value for r is 114 therefore this checks if the first value recieved is a r which would move the right servo
    if (varCode == 114 && loopLap == 0) {
      getRight = 1;
      loopLap = 1;
    }
    //ascii value or l is 108 therefore this checks if the first value recieved is a l which would move the left servo
    else if (varCode == 108 && loopLap == 0) {
      getLeft = 1;
      loopLap = 1;
    }
    //ascii value for a is 97 therefore this checks if the first value recieved is a la which would move the arm servo
    else if (varCode == 97 && loopLap == 0) {
      getArm = 1;
      loopLap = 1;
    }
    //this code runs if first value is r
    if (getRight == 1) {
      char ch = Serial.read();
      if (ch >= '0' && ch <= '9') {
        value = (value * 10) + (ch - '0');
        //value of 1000
        //value = (0*10) + 49-48 value = 1
        //value = (1*10) + 48-48 value = 10
        //value = (10*10) + 48-48 value = 100
        //value = (100*10) + 48-48 value = 1000
        //value of 2000
        //value = (0*10) + 50-48 value = 2
        //value = (2*10) + 48-48 value = 20
        //value = (20*10) + 48-48 value = 200
        //value = (200*10) + 48-48 value = 2000
      }
      else if (ch == 10) {
        setServoRight(value);
        value = 0;
        getRight=0;
        loopLap=0;
      }
    }
    //this code runs if first value is l
    else if (getLeft == 1) {
      char ch = Serial.read();
      if (ch >= '0' && ch <= '9') {
        value = (value * 10) + (ch - '0');
      }
      else if (ch == 10) {
        setServoLeft(value);
        value = 0;
        getLeft=0;
        loopLap=0;
      }
    }
    else if (getArm == 1) {
      char ch = Serial.read();
      if (ch >= '0' && ch <= '9') {
        value = (value * 10) + (ch - '0');
      }
      else if (ch == 10) {
        setArmServo(value);
        value = 0;
        getArm=0;
        loopLap=0;
      }
    }
  }
}
void setServoRight(int value) {
  rightservo.writeMicroseconds(value);
}
void setServoLeft(int value) {
  leftservo.writeMicroseconds(value);
}
void setArmServo(int value) {
  armservo.writeMicroseconds(value);
}
