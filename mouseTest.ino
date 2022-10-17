#include <Adafruit_MotorShield.h>
#define ENCODER_1A   2
#define ENCODER_1B   3
#define ENCODER_2A   6
#define ENCODER_2B   7
#define ENCODER_3A   4
#define ENCODER_3B   5
#define ENCODER_4A   8
#define ENCODER_4B   9
#define frontDistance A3
#define backDistance A1
#define rightDistance A2
#define leftDistance A0
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *topLeft = AFMS.getMotor(1);
Adafruit_DCMotor *bottomLeft = AFMS.getMotor(2);
Adafruit_DCMotor *bottomRight = AFMS.getMotor(3);
Adafruit_DCMotor *topRight = AFMS.getMotor(4);
volatile float topRightDistance = 0;
volatile float topLeftDistance = 0;
volatile float bottomRightDistance = 0;
volatile float bottomLeftDistance = 0;
const int velocity = 125;
const int counterClockwiseValue = 1650;
const int clockwiseValue = counterClockwiseValue;
const int wallDistance = 800;
const int frontWallDistance = 760;
const int rightWallDistance = 830;
const int backWallDistance = 720;
const int leftWallDistance = 760;
const int rightWallCorrection = 850;
const int leftWallCorrection = 820;
const int frontWallCorrection = 850;
const int unitDistance = 3550;
const float correctionRate = 1.20;
bool northWall, eastWall, southWall, westWall;
bool checkNorthWall(int orientation) {
  int northDistance;
  switch (orientation) {
    case 0: {
      int fD1=0, fD2=0, fD3=0;
      delay(10);
      while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
      while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
      while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
      if (fD1 > fD2 && fD1 < fD3) { northDistance = fD1; }
      else if (fD2 > fD1 && fD2 < fD3) { northDistance = fD2; }
      else { northDistance = fD3; }
      if (northDistance>frontWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 1: {
      int lD1=0, lD2=0, lD3=0;
      delay(10);
      while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
      while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
      while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
      if (lD1 > lD2 && lD1 > lD3) { northDistance = lD1; }
      else if (lD2 > lD1 && lD2 > lD3) { northDistance = lD2; }
      else { northDistance = lD3; }
      if (northDistance>leftWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 2: {
      int bD1=0, bD2=0, bD3=0;
      delay(10);
      while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
      while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
      while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
      if (bD1 > bD2 && bD1 > bD3) { northDistance = bD1; }
      else if (bD2 > bD1 && bD2 > bD3) { northDistance = bD2; }
      else { northDistance = bD3; }
      if (northDistance>backWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 3: {
      int rD1=0, rD2=0, rD3=0;
      delay(10);
      while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
      while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
      while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
      if (rD1 > rD2 && rD1 > rD3) { northDistance = rD1; }
      else if (rD2 > rD1 && rD2 > rD3) { northDistance = rD2; }
      else { northDistance = rD3; }
      if (northDistance>rightWallDistance) { return true; }
      else { return false; }
      break;
    }
  }
}
bool checkEastWall(int orientation) {
  int eastDistance;
  switch (orientation) {
    case 1: {
      int fD1=0, fD2=0, fD3=0;
      delay(10);
      while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
      while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
      while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
      if (fD1 > fD2 && fD1 > fD3) { eastDistance = fD1; }
      else if (fD2 > fD1 && fD2 > fD3) { eastDistance = fD2; }
      else { eastDistance = fD3; }
      if (eastDistance>frontWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 2: {
      int lD1=0, lD2=0, lD3=0;
      delay(10);
      while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
      while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
      while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
      if (lD1 > lD2 && lD1 > lD3) { eastDistance = lD1; }
      else if (lD2 > lD1 && lD2 > lD3) { eastDistance = lD2; }
      else { eastDistance = lD3; }
      if (eastDistance>leftWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 3: {
      int bD1=0, bD2=0, bD3=0;
      delay(10);
      while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
      while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
      while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
      if (bD1 > bD2 && bD1 > bD3) { eastDistance = bD1; }
      else if (bD2 > bD1 && bD2 > bD3) { eastDistance = bD2; }
      else { eastDistance = bD3; }
      if (eastDistance>backWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 0: {
      int rD1=0, rD2=0, rD3=0;
      delay(10);
      while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
      while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
      while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
      if (rD1 > rD2 && rD1 > rD3) { eastDistance = rD1; }
      else if (rD2 > rD1 && rD2 > rD3) { eastDistance = rD2; }
      else { eastDistance = rD3; }
      if (eastDistance>rightWallDistance) { return true; }
      else { return false; }
      break;
    }
  }
}
bool checkSouthWall(int orientation) {
  int southDistance;
  switch (orientation) {
    case 2: {
      int fD1=0, fD2=0, fD3=0;
      delay(10);
      while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
      while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
      while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
      if (fD1 > fD2 && fD1 > fD3) { southDistance = fD1; }
      else if (fD2 > fD1 && fD2 > fD3) { southDistance = fD2; }
      else { southDistance = fD3; }
      if (southDistance>frontWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 3: {
      int lD1=0, lD2=0, lD3=0;
      delay(10);
      while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
      while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
      while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
      if (lD1 > lD2 && lD1 > lD3) { southDistance = lD1; }
      else if (lD2 > lD1 && lD2 > lD3) { southDistance = lD2; }
      else { southDistance = lD3; }
      if (southDistance>leftWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 0: {
      int bD1=0, bD2=0, bD3=0;
      delay(10);
      while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
      while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
      while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
      if (bD1 > bD2 && bD1 > bD3) { southDistance = bD1; }
      else if (bD2 > bD1 && bD2 > bD3) { southDistance = bD2; }
      else { southDistance = bD3; }
      if (southDistance>backWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 1: {
      int rD1=0, rD2=0, rD3=0;
      delay(10);
      while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
      while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
      while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
      if (rD1 > rD2 && rD1 > rD3) { southDistance = rD1; }
      else if (rD2 > rD1 && rD2 > rD3) { southDistance = rD2; }
      else { southDistance = rD3; }
      if (southDistance>rightWallDistance) { return true; }
      else { return false; }
      break;
    }
  }
}
bool checkWestWall(int orientation) {
  int westDistance;
  switch (orientation) {
    case 3: {
      int fD1=0, fD2=0, fD3=0;
      delay(10);
      while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
      while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
      while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
      if (fD1 > fD2 && fD1 > fD3) { westDistance = fD1; }
      else if (fD2 > fD1 && fD2 > fD3) { westDistance = fD2; }
      else { westDistance = fD3; }
      if (westDistance>frontWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 0: {
      int lD1=0, lD2=0, lD3=0;
      delay(10);
      while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
      while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
      while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
      if (lD1 > lD2 && lD1 > lD3) { westDistance = lD1; }
      else if (lD2 > lD1 && lD2 > lD3) { westDistance = lD2; }
      else { westDistance = lD3; }
      if (westDistance>leftWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 1: {
      int bD1=0, bD2=0, bD3=0;
      delay(10);
      while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
      while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
      while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
      if (bD1 > bD2 && bD1 > bD3) { westDistance = bD1; }
      else if (bD2 > bD1 && bD2 > bD3) { westDistance = bD2; }
      else { westDistance = bD3; }
      if (westDistance>backWallDistance) { return true; }
      else { return false; }
      break;
    }
    case 2: {
      int rD1=0, rD2=0, rD3=0;
      delay(10);
      while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
      while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
      while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
      if (rD1 > rD2 && rD1 > rD3) { westDistance = rD1; }
      else if (rD2 > rD1 && rD2 > rD3) { westDistance = rD2; }
      else { westDistance = rD3; }
      if (westDistance>rightWallDistance) { return true; }
      else { return false; }
      break;
    }
  }
}
int getFollowDirection() {
  int rightWallDistance, leftWallDistance;
  int rD1=0, rD2=0, rD3=0;
  delay(50);
  while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
  while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
  while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
  if (rD1 > rD2 && rD1 < rD3) { rightWallDistance = rD1; }
  else if (rD2 > rD1 && rD2 < rD3) { rightWallDistance = rD2; }
  else { rightWallDistance = rD3; }
  int lD1=0, lD2=0, lD3=0;
  delay(50);
  while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
  while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
  while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
  if (lD1 > lD2 && lD1 < lD3) { leftWallDistance = lD1; }
  else if (lD2 > lD1 && lD2 < lD3) { leftWallDistance = lD2; }
  else { leftWallDistance = lD3; }
  if (rightWallDistance>leftWallDistance) { return 0; }
  else { return 1; }
}
bool correctFront() {
  int frontWallDistance;
  int fD1=0, fD2=0, fD3=0;
  delay(10);
  while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
  while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
  while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
  if (fD1 > fD2 && fD1 > fD3) { frontWallDistance = fD1; }
  else if (fD2 > fD1 && fD2 > fD3) { frontWallDistance = fD2; }
  else { frontWallDistance = fD3; }
  if (frontWallDistance>frontWallCorrection) { return true; }
  else { return false; }
}
double getRightDistance() {
  int rightWallDistance;
  int rD1=0, rD2=0, rD3=0;
  delay(50);
  while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
  while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
  while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
  if (rD1 > rD2 && rD1 < rD3) { rightWallDistance = rD1; }
  else if (rD2 > rD1 && rD2 < rD3) { rightWallDistance = rD2; }
  else { rightWallDistance = rD3; }
  double actualDistance = 0.0002*(rightWallDistance*rightWallDistance)-0.3339*rightWallDistance+150.15;
  return actualDistance;
}
double getLeftDistance() {
  int leftWallDistance;
  int lD1=0, lD2=0, lD3=0;
  delay(50);
  while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
  while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
  while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
  if (lD1 > lD2 && lD1 < lD3) { leftWallDistance = lD1; }
  else if (lD2 > lD1 && lD2 < lD3) { leftWallDistance = lD2; }
  else { leftWallDistance = lD3; }
  double actualDistance = 0.0002*(leftWallDistance*leftWallDistance)-0.3101*leftWallDistance+138.73;
  return actualDistance;
}
int getFrontDistance() {
  int frontWallDistance;
  int fD1=0, fD2=0, fD3=0;
  delay(50);
  while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
  while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
  while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
  if (fD1 > fD2 && fD1 > fD3) { frontWallDistance = fD1; }
  else if (fD2 > fD1 && fD2 > fD3) { frontWallDistance = fD2; }
  else { frontWallDistance = fD3; }
  return frontWallDistance;
}
void stopMotors() {
  topRight->setSpeed(0);
  topLeft->setSpeed(0);
  bottomRight->setSpeed(0);
  bottomLeft->setSpeed(0);
  return;
}
void followRightWall() {
  int rightWallDistance;
  topRight->run(FORWARD);
  topLeft->run(FORWARD);
  bottomRight->run(FORWARD);
  bottomLeft->run(FORWARD);
  rightWallDistance = getRightDistance();
  if (rightWallDistance>825) {
    topRight->setSpeed(velocity*correctionRate);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity*correctionRate);
    bottomLeft->setSpeed(velocity);
  }
  else if (rightWallDistance<750) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity*correctionRate);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity*correctionRate);
  }
  else {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity);
  }
}
void followLeftWall() {
  int leftWallDistance;
  topRight->run(FORWARD);
  topLeft->run(FORWARD);
  bottomRight->run(FORWARD);
  bottomLeft->run(FORWARD);
  leftWallDistance = getLeftDistance();
  if (leftWallDistance>775) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity*correctionRate);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity*correctionRate);
  }
  else if (leftWallDistance<725) {
    topRight->setSpeed(velocity*correctionRate);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity*correctionRate);
    bottomLeft->setSpeed(velocity);
  }
  else {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity);
  }
}
void goForward() {
  int average;
  double rightWallDistance, leftWallDistance;
  topRight->run(FORWARD);
  topLeft->run(FORWARD);
  bottomRight->run(FORWARD);
  bottomLeft->run(FORWARD);
  rightWallDistance = getRightDistance();
  leftWallDistance = getLeftDistance();
  if (rightWallDistance>10 || leftWallDistance>10) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity);
  }
  if (rightWallDistance>leftWallDistance+3) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity*correctionRate);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity*correctionRate);
  }
  else if (leftWallDistance>rightWallDistance+3) {
    topRight->setSpeed(velocity*correctionRate);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity*correctionRate);
    bottomLeft->setSpeed(velocity);
  }
  else {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity);
  }
  return;
}
void goBackward() {
  topRight->run(BACKWARD);
  topLeft->run(BACKWARD);
  bottomRight->run(BACKWARD);
  bottomLeft->run(BACKWARD);
  topRight->setSpeed(velocity);
  topLeft->setSpeed(velocity);
  bottomRight->setSpeed(velocity);
  bottomLeft->setSpeed(velocity);
  return;
}
void turnClockwise() {
  int average;
  topRight->run(BACKWARD);
  topLeft->run(FORWARD);
  bottomRight->run(BACKWARD);
  bottomLeft->run(FORWARD);
  topRight->setSpeed(velocity);
  topLeft->setSpeed(velocity);
  bottomRight->setSpeed(velocity);
  bottomLeft->setSpeed(velocity);
  average = (topLeftDistance+bottomLeftDistance)/2;
  while (average<clockwiseValue) {
    average = (topLeftDistance+bottomLeftDistance)/2;
  }
  stopMotors();
  resetDistances();
  return;
}
void turnCounterClockwise() {
  int average;
  topRight->run(FORWARD);
  topLeft->run(BACKWARD);
  bottomRight->run(FORWARD);
  bottomLeft->run(BACKWARD);
  topRight->setSpeed(velocity);
  topLeft->setSpeed(velocity);
  bottomRight->setSpeed(velocity);
  bottomLeft->setSpeed(velocity);
  average = (topRightDistance+bottomRightDistance)/2;
  while (average<counterClockwiseValue) {
    average = (topRightDistance+bottomRightDistance)/2;
  }
  stopMotors();
  resetDistances();
  return;
}
void goNorth(int orientation) {
  int average;
  switch (orientation) {
    case 0:
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      break;
    case 1:
      turnCounterClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      break;
    case 2:
      goBackward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      break;
    case 3:
      goForward();
      turnClockwise();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
        while (average<unitDistance) {
          average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
        }
        stopMotors();
        resetDistances();
        if (correctFront()) {
          goBackward();
          delay(250);
          stopMotors();
          resetDistances();
        }
        break;
  }
  return;
}
void updateTopRightDistance() {topRightDistance++;}
void updateTopLeftDistance() {topLeftDistance++;}
void updateBottomRightDistance() {bottomRightDistance++;}
void updateBottomLeftDistance() {bottomLeftDistance++;}

void resetDistances() {
  topRightDistance = 0;
  topLeftDistance = 0;
  bottomRightDistance = 0;
  bottomLeftDistance = 0;
}

void setup() {
  //Serial.begin(9600);
  
  pinMode(ENCODER_1A, INPUT_PULLUP);
  pinMode(ENCODER_1B, INPUT_PULLUP);
  pinMode(ENCODER_2A, INPUT_PULLUP);
  pinMode(ENCODER_2B, INPUT_PULLUP);
  pinMode(ENCODER_3A, INPUT_PULLUP);
  pinMode(ENCODER_3B, INPUT_PULLUP);
  pinMode(ENCODER_4A, INPUT_PULLUP);
  pinMode(ENCODER_4B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCODER_1A), updateTopRightDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_1B), updateTopRightDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_2A), updateTopLeftDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_2B), updateTopLeftDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_3A), updateBottomRightDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_3B), updateBottomRightDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_4A), updateBottomLeftDistance, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENCODER_4B), updateBottomLeftDistance, CHANGE);
  
  AFMS.begin();

  stopMotors();
  
  delay(5000);
  goNorth(0);
  delay(5);
  turnCounterClockwise();
  delay(5);
  goNorth(0);
  goNorth(0);
  goNorth(0);
  goNorth(0);
  while (getFrontDistance()<800) { goForward(); }
  stopMotors();
  resetDistances();
  delay(5);
  turnClockwise();
  delay(5);
  goNorth(0);
  goNorth(0);
  while (getFrontDistance()<800) { goForward(); }
  stopMotors();
  resetDistances();
  delay(5);
  turnCounterClockwise();
  goNorth(0);
  goNorth(0);
  delay(5);
  turnCounterClockwise();
  delay(5);
  goNorth(0);
  goNorth(0);
  delay(5);
  turnClockwise();
  delay(5);
  goNorth(0);
  delay(5);
  turnClockwise();
  delay(5);
  goNorth(0);
  goNorth(0);
  goNorth(0);
  turnClockwise();
  goNorth(0);
  goNorth(0);
}
void loop() {}
