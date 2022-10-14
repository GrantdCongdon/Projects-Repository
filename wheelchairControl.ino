//include motor shield library
#include <AFMotor.h>
//create motor objects from library to drive wheelchair
AF_DCMotor rightMotor(2, MOTOR12_64KHZ);
AF_DCMotor leftMotor(1, MOTOR12_64KHZ);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(9, INPUT);
  rightMotor.setSpeed(100);
  leftMotor.setSpeed(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0) {
    int data = Serial.read();
    if (data==102 && digitalRead(9)==LOW) {
      rightMotor.run(FORWARD);
      leftMotor.run(FORWARD);
    }
    else if (data==115 && digitalRead(9)==LOW) {
      rightMotor.run(RELEASE);
      leftMotor.run(RELEASE);
    }
     else if (data==108 && digitalRead(9)==LOW) {
      //run the left motor only, turn off right
      rightMotor.run(RELEASE);
      leftMotor.run(FORWARD);
    }
    //is the value b is recieved
    else if (data==98 && digitalRead(9)==LOW) {
      //drive both backwards
      rightMotor.run(BACKWARD);
      leftMotor.run(BACKWARD);
    }
    //if s is recieved
    else if (data==115 && digitalRead(9)==LOW) {
      //stop both motors
      rightMotor.run(RELEASE);
      leftMotor.run(RELEASE);
    }
    //if the value r is recieved
    else if (data==114 && digitalRead(9)==LOW) {
      //run the right motor forward, turn off the left
      rightMotor.run(FORWARD);
      leftMotor.run(RELEASE);
    }
  }
}
