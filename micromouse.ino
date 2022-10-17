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
int archiveDistance;

bool correctedRightForwards = false;
bool correctedLeftForwards = false;
bool correctedRightBackwards = false;
bool correctedLeftBackwards = false;

const int velocity = 150;
const int counterClockwiseValue = 1700;
const int clockwiseValue = counterClockwiseValue;

const int frontWallDistance = 560;
const int rightWallDistance = 590;
const int backWallDistance = 565;
const int leftWallDistance = 600;

const int rightWallCorrection = 850;
const int leftWallCorrection = 800;
const int frontWallCorrection = 775;
const int backWallCorrection = 775;

const int unitDistance = 3500;
const float correctionRate = 1.2;
const float overCorrectionRate = 1.1;
const int mazeSize = 10;
int maze[mazeSize][mazeSize];
int maze1[mazeSize][mazeSize];
int maze2[mazeSize][mazeSize];
int orientation = 0;
bool northWall, eastWall, southWall, westWall;
bool foundMiddle;
int wallIndex;
int location[2];
int findLocationY(int maze[][mazeSize], int value) {
  for (int i=0; i<mazeSize; i++) {
    for (int e=0; e<mazeSize; e++) {
      if (maze[i][e]==value) {
        return i;
      }
    }
  }
}
int findLocationX(int maze[][mazeSize], int value) {
  for (int i=0; i<mazeSize; i++) {
    for (int e=0; e<mazeSize; e++) {
      if (maze[i][e]==value) {
        return e;
      }
    }
  }
}
bool checkNorthWall(int orientation) {
  int northDistance;
  if (maze[location[0]-1][location[1]]==17) { return true; }
  switch (orientation) {
    case 0: {
      int fD1=0, fD2=0, fD3=0;
      delay(10);
      while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
      while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
      while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
      if (fD1 > fD2 && fD1 > fD3) { northDistance = fD1; }
      else if (fD2 > fD1 && fD2 > fD3) { northDistance = fD2; }
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
  if (maze[location[0]][location[1]+1]==17) { return true; }
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
  if (maze[location[0]+1][location[1]]==17) { return true; }
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
  if (maze[location[0]][location[1]-1]==17) { return true; }
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
int getWallIndex(int orientation) {
  northWall = checkNorthWall(orientation);
  eastWall = checkEastWall(orientation);
  southWall = checkSouthWall(orientation);
  westWall = checkWestWall(orientation);
  if (northWall && checkSouthWall(orientation) && checkEastWall(orientation) && checkWestWall(orientation)) { return 14; }
  else if (!northWall && southWall && eastWall && westWall) { return 10; }
  else if (northWall && !southWall && eastWall && westWall) { return 12; }
  else if (northWall && southWall && !eastWall && westWall) { return 11; }
  else if (northWall && southWall && eastWall && !westWall) { return 13; }
  else if (!northWall && !southWall && eastWall && westWall) { return 9; }
  else if (!northWall && southWall && !eastWall && westWall) { return 8; }
  else if (!northWall && southWall && eastWall && !westWall) { return 7; }
  else if (northWall && !southWall && !eastWall && westWall) { return 6; }
  else if (northWall && !southWall && eastWall && !westWall) { return 4; }
  else if (northWall && southWall && !eastWall && !westWall) { return 5; }
  else if (northWall && !southWall && !eastWall && !westWall) { return 0; }
  else if (!northWall && southWall && !eastWall && !westWall) { return 2; }
  else if (!northWall && !southWall && eastWall && !westWall) { return 1; }
  else if (!northWall && !southWall && !eastWall && westWall) { return 3; }
  else if (!northWall && !southWall && !eastWall && !westWall) { return 15; }
  else { return -1; }
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
bool correctBack() {
  int backWallDistance;
  int bD1=0, bD2=0, bD3=0;
  delay(10);
  while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
  while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
  while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
  if (bD1 > bD2 && bD1 > bD3) { backWallDistance = bD1; }
  else if (bD2 > bD1 && bD2 > bD3) { backWallDistance = bD2; }
  else { backWallDistance = bD3; }
  if (backWallDistance>backWallCorrection) { return true; }
  else { return false; }
}
double getRightDistance() {
  int rightWallDistance;
  int rD1=0, rD2=0, rD3=0;
  delay(50);
  while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
  while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
  while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
  if (rD1 > rD2 && rD1 > rD3) { rightWallDistance = rD1; }
  else if (rD2 > rD1 && rD2 > rD3) { rightWallDistance = rD2; }
  else { rightWallDistance = rD3; }
  return rightWallDistance;
}
double getLeftDistance() {
  int leftWallDistance;
  int lD1=0, lD2=0, lD3=0;
  delay(50);
  while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
  while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
  while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
  if (lD1 > lD2 && lD1 > lD3) { leftWallDistance = lD1; }
  else if (lD2 > lD1 && lD2 > lD3) { leftWallDistance = lD2; }
  else { leftWallDistance = lD3; }
  return leftWallDistance;
}
void stopMotors() {
  topRight->setSpeed(0);
  topLeft->setSpeed(0);
  bottomRight->setSpeed(0);
  bottomLeft->setSpeed(0);
  return;
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
  if (correctedRightForwards && leftWallDistance<leftWallCorrection) {
    topRight->setSpeed(velocity*overCorrectionRate);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity*overCorrectionRate);
    bottomLeft->setSpeed(velocity);
    correctedRightForwards = false;
  }
  else if (correctedLeftForwards && rightWallDistance<rightWallCorrection) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity*overCorrectionRate);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity*overCorrectionRate);
    correctedLeftForwards = false;
  }
  else {
    if (leftWallDistance>leftWallCorrection) {
      topRight->setSpeed(velocity);
      topLeft->setSpeed(velocity*correctionRate);
      bottomRight->setSpeed(velocity);
      bottomLeft->setSpeed(velocity*correctionRate);
      correctedRightForwards = true;
    }
    else if (rightWallDistance>rightWallCorrection) {
      topRight->setSpeed(velocity*correctionRate);
      topLeft->setSpeed(velocity);
      bottomRight->setSpeed(velocity*correctionRate);
      bottomLeft->setSpeed(velocity);
      correctedLeftForwards = true;
    }
    else {
      topRight->setSpeed(velocity);
      topLeft->setSpeed(velocity);
      bottomRight->setSpeed(velocity);
      bottomLeft->setSpeed(velocity);
    }
  }
  return;
}
void goBackward() {
  int average;
  double rightWallDistance, leftWallDistance;
  topRight->run(BACKWARD);
  topLeft->run(BACKWARD);
  bottomRight->run(BACKWARD);
  bottomLeft->run(BACKWARD);
  rightWallDistance = getRightDistance();
  leftWallDistance = getLeftDistance();
  if (correctedRightBackwards && leftWallDistance<leftWallCorrection) {
    topRight->setSpeed(velocity*overCorrectionRate);
    topLeft->setSpeed(velocity);
    bottomRight->setSpeed(velocity*overCorrectionRate);
    bottomLeft->setSpeed(velocity);
    correctedRightBackwards = false;
  }
  else if (correctedLeftBackwards && rightWallDistance<rightWallCorrection) {
    topRight->setSpeed(velocity);
    topLeft->setSpeed(velocity*overCorrectionRate);
    bottomRight->setSpeed(velocity);
    bottomLeft->setSpeed(velocity*overCorrectionRate);
    correctedLeftBackwards = false;
  }
  else {
    if (leftWallDistance>leftWallCorrection) {
      topRight->setSpeed(velocity);
      topLeft->setSpeed(velocity*correctionRate);
      bottomRight->setSpeed(velocity);
      bottomLeft->setSpeed(velocity*correctionRate);
      correctedRightBackwards = true;
    }
    else if (rightWallDistance>rightWallCorrection) {
      topRight->setSpeed(velocity*correctionRate);
      topLeft->setSpeed(velocity);
      bottomRight->setSpeed(velocity*correctionRate);
      bottomLeft->setSpeed(velocity);
      correctedLeftBackwards = true;
    }
    else {
      topRight->setSpeed(velocity);
      topLeft->setSpeed(velocity);
      bottomRight->setSpeed(velocity);
      bottomLeft->setSpeed(velocity);
    }
  }
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
  average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
  while (average<clockwiseValue) {
    average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
  }
  stopMotors();
  resetDistances();
  orientation = (orientation+1>3) ? 0 : orientation+1;
  return;
}
void inchClockwise() {
  topRight->run(BACKWARD);
  topLeft->run(FORWARD);
  bottomRight->run(BACKWARD);
  bottomLeft->run(FORWARD);
  topRight->setSpeed(velocity/2);
  topLeft->setSpeed(velocity/2);
  bottomRight->setSpeed(velocity/2);
  bottomLeft->setSpeed(velocity/2);
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
  average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
  while (average<counterClockwiseValue) {
    average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
  }
  stopMotors();
  resetDistances();
  orientation = (orientation-1<0) ? 3 : orientation-1;
  return;
}
void inchCounterClockwise() {
  topRight->run(FORWARD);
  topLeft->run(BACKWARD);
  bottomRight->run(FORWARD);
  bottomLeft->run(BACKWARD);
  topRight->setSpeed(velocity/2);
  topLeft->setSpeed(velocity/2);
  bottomRight->setSpeed(velocity/2);
  bottomLeft->setSpeed(velocity/2);
}
void moveNorth(int orientation) {
  int average, startDistance;
  switch (orientation) {
    case 0:
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkNorthWall(0)) {
        goForward();
        while (!correctFront()) {}
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
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkNorthWall(0)) {
        goForward();
        while (!correctFront()) {}
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
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctBack()) {
        goForward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkNorthWall(2)) {
        goBackward();
        while (!correctBack()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 3:
      turnClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkNorthWall(0)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
  }
  return;
}
void moveEast(int orientation) {
  int average;
  switch (orientation) {
    case 0:
      turnClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkEastWall(1)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 1:
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkEastWall(1)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 2:
      turnCounterClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkEastWall(1)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 3:
      goBackward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctBack()) {
        goForward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkEastWall(3)) {
        goBackward();
        while (!correctBack()) {}
        stopMotors();
        resetDistances();
      }
      break;
  }
  return;
}
void moveSouth(int orientation) {
  int average;
  switch (orientation) {
    case 0:
      goBackward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctBack()) {
        goForward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkSouthWall(0)) {
        goBackward();
        while (!correctBack()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 1:
      turnClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkSouthWall(2)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 2:
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkSouthWall(2)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 3:
      turnCounterClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkSouthWall(2)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
  }
  return;
}
void moveWest(int orientation) {
  int average;
  switch (orientation) {
    case 0:
      turnCounterClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkWestWall(3)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 1:
      goBackward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctBack()) {
        goForward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkWestWall(1)) {
        goBackward();
        while (!correctBack()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 2:
      turnClockwise();
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkWestWall(3)) {
        goForward();
        while (!correctFront()) {}
        stopMotors();
        resetDistances();
      }
      break;
    case 3:
      goForward();
      average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      while (average<unitDistance) {
        average = (topRightDistance+topLeftDistance+bottomRightDistance+bottomLeftDistance)/4;
      }
      stopMotors();
      archiveDistance = topRightDistance;
      resetDistances();
      if (correctFront()) {
        goBackward();
        delay(250);
        stopMotors();
        resetDistances();
      }
      else if (checkWestWall(3)) {
        goForward();
        while (!correctFront()) {}
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

/*void writeToServerint message) {
  String sMessage = String(message);
  while (!client) { client = server.available(); }
  while (client.connected()) {
    if (client.available()) {
      String currentLine = "";
      char c = client.read();
      if (c=='\n') {
        if (currentLine.length()==0) {
          client.println();
          client.println("<h2>"+sMessage+"</h2>");
          client.println();
          break;
        }
        else {
          currentLine="";
        }
      }
    }
  }
}*/
void goNorth() {
  while (!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) {
    if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
      foundMiddle = true;
      break;
    }
    if ((eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
      maze[location[0]][location[1]] = 17;
    }
    else {
       maze[location[0]][location[1]] = wallIndex;
    }
    moveNorth(orientation);
    location[0]--;
    //maze[location[0]][location[1]] = 42;
    wallIndex = getWallIndex(orientation);
    northWall = checkNorthWall(orientation);
    eastWall = checkEastWall(orientation);
    southWall = checkSouthWall(orientation);
    westWall = checkWestWall(orientation);
    if ((!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) || (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) && maze[location[0]-1][location[1]]!=16) {
      if (!eastWall && !westWall) {
        switch (archiveDistance%2) {
          case 0:
            if (!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                  maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveEast(orientation);
              location[1]++;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
          case 1:
            if (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveWest(orientation);
              location[1]--;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
        }
      }
      else if (!eastWall) {
        if (!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
             maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveEast(orientation);
          location[1]++;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      else {
        if (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveWest(orientation);
          location[1]--;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      break;
    }
  }
}
void goEast() {
  while (!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) {
    if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
      foundMiddle = true;
      break;
    }
    if ((northWall || maze[location[0]-1][location[1]]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
      maze[location[0]][location[1]] = 17;
    }
    else {
      maze[location[0]][location[1]] = wallIndex;
    }
    moveEast(orientation);
    location[1]++;
    //maze[location[0]][location[1]] = 42;
    wallIndex = getWallIndex(orientation);
    northWall = checkNorthWall(orientation);
    eastWall = checkEastWall(orientation);
    southWall = checkSouthWall(orientation);
    westWall = checkWestWall(orientation);
    if (((!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) || (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18)) && maze[location[0]][location[1]+1]!=16) {
      if (!northWall && !southWall) {
        switch (archiveDistance%2) {
          case 0:
            if (!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveNorth(orientation);
              location[0]--;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
          case 1:
            if (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveSouth(orientation);
              location[0]++;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
        }
      }
      else if (!northWall) {
        if (!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveNorth(orientation);
          location[0]--;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      else {
        if (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveSouth(orientation);
          location[0]++;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      break;
    }
  }
}
void goSouth() {
  while (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18) {
    if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
      foundMiddle = true;
      break;
    }
    if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
      maze[location[0]][location[1]] = 17;
    }
    else {
      maze[location[0]][location[1]] = wallIndex;
    }
    moveSouth(orientation);
    location[0]++;
    //maze[location[0]][location[1]] = 42;
    wallIndex = getWallIndex(orientation);
    northWall = checkNorthWall(orientation);
    eastWall = checkEastWall(orientation);
    southWall = checkSouthWall(orientation);
    westWall = checkWestWall(orientation);
    if (((!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) || (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18)) && maze[location[0]+1][location[1]]!=16) {
      if (!eastWall && !westWall) {
        switch (archiveDistance%2) {
          case 0:
            if (!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveEast(orientation);
              location[1]++;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
          case 1:
            if (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveWest(orientation);
              location[1]--;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
        }
      }
      else if (!eastWall) {
        if (!eastWall && maze[location[0]][location[1]+1]!=17 && maze[location[0]][location[1]+1]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveEast(orientation);
          location[1]++;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      else {
        if (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveWest(orientation);
          location[1]--;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      break;
    }
  }
}
void goWest() {
  while (!westWall && maze[location[0]][location[1]-1]!=17 && maze[location[0]][location[1]-1]!=18) {
    if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
      foundMiddle = true;
      break;
    }
    if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17)) {
      maze[location[0]][location[1]] = 17;
    }
    else {
      maze[location[0]][location[1]] = wallIndex;
    }
    moveWest(orientation);
    location[1]--;
    //maze[location[0]][location[1]] = 42;
    wallIndex = getWallIndex(orientation);
    northWall = checkNorthWall(orientation);
    eastWall = checkEastWall(orientation);
    southWall = checkSouthWall(orientation);
    westWall = checkWestWall(orientation);
    if (((!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) || (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18)) && maze[location[0]][location[1]-1]!=16) {
      if (!northWall && !southWall) {
        switch (archiveDistance%2) {
          case 0:
            if (!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveNorth(orientation);
              location[0]--;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
          case 1:
            if (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18) {
              if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
                foundMiddle = true;
                break;
              }
              if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
                maze[location[0]][location[1]] = 17;
              }
              else {
                maze[location[0]][location[1]] = wallIndex;
              }
              moveSouth(orientation);
              location[0]++;
              //maze[location[0]][location[1]] = 42;
              wallIndex = getWallIndex(orientation);
              northWall = checkNorthWall(orientation);
              eastWall = checkEastWall(orientation);
              southWall = checkSouthWall(orientation);
              westWall = checkWestWall(orientation);
            }
            break;
        }
      }
      else if (!northWall) {
        if (!northWall && maze[location[0]-1][location[1]]!=17 && maze[location[0]-1][location[1]]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((eastWall || maze[location[0]][location[1]+1]==17) && (southWall || maze[location[0]+1][location[1]]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveNorth(orientation);
          location[0]--;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      else {
        if (!southWall && maze[location[0]+1][location[1]]!=17 && maze[location[0]+1][location[1]]!=18) {
          if ((location[0]==mazeSize/2 || location[0]==mazeSize/2-1) && (location[1]==mazeSize/2 || location[1]==mazeSize/2-1)) {
            foundMiddle = true;
            break;
          }
          if ((northWall || maze[location[0]-1][location[1]]==17) && (eastWall || maze[location[0]][location[1]+1]==17) && (westWall || maze[location[0]][location[1]-1]==17)) {
            maze[location[0]][location[1]] = 17;
          }
          else {
            maze[location[0]][location[1]] = wallIndex;
          }
          moveSouth(orientation);
          location[0]++;
          //maze[location[0]][location[1]] = 42;
          wallIndex = getWallIndex(orientation);
          northWall = checkNorthWall(orientation);
          eastWall = checkEastWall(orientation);
          southWall = checkSouthWall(orientation);
          westWall = checkWestWall(orientation);
        }
      }
      break;
    }
  }
}
void setup() {
  /*while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  server.begin();
  client = server.available();
  while (!client) { client = server.available(); }
  while (client.connected()) {
    if (client.available()) {
      String currentLine = "";
      char c = client.read();
      if (c=='\n') {
        if (currentLine.length()==0) {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println();
          client.println("<h1>Online Log</h1>");
          client.println();
          break;
        }
        else {
          currentLine="";
        }
      }
    }
  }*/
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
  
  delay(3000);
  for (int i=0; i<mazeSize; i++) {
    for (int e=0; e<mazeSize; e++) {
      maze[i][e] = 16;
    }
  }
  //maze[5][5]=69; maze[5][4]=69; maze[4][4]=69; maze[4][5]=69;
  while (checkNorthWall(0)) {
    turnClockwise();
    orientation++;
    if (orientation>3) { orientation=0; }
  }
  //maze[mazeSize-1][mazeSize-1]=42;
  location[0] = mazeSize-1;
  location[1] = mazeSize-1;
  int x=0, y=0;
  /*switch (orientation) {
    case 0: {
      maze1[mazeSize-1][0] = 18;
      maze2[mazeSize-1][mazeSize-1] = 18;
      while (!northWall) {
        moveNorth(orientation);
        wallIndex = getWallIndex(orientation);
        if (eastWall && checkWestWall(orientation) && (maze1[mazeSize-y][0]==18 || maze1[mazeSize-y][0]==17) && (maze2[mazeSize-y][mazeSize-1]==18 || maze2[mazeSize-y][mazeSize-1]==17)) {
            maze1[mazeSize-1-y][0] = 17; //West
            maze2[mazeSize-1-y][mazeSize-1] = 17; //East
         }
         else {
            maze1[mazeSize-1-y][0] = wallIndex; //West
            maze2[mazeSize-1-y][mazeSize-1] = wallIndex; //East
        }
        if (!eastWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze1[i][e];
            }
          }
          maze[mazeSize-1-y][0] = 42; break;
        }
        else if (!westWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze2[i][e];
            }
          }
          maze[mazeSize-1-y][mazeSize-1] = 42; break;
        }
      }
      break;
    }
    case 1: {
      ////writeToServer1);
      maze1[0][0] = 18;
      maze2[mazeSize-1][0] = 18;
      while (!eastWall) {
        moveEast(orientation);
        wallIndex = getWallIndex(orientation);
        if (northWall && checkSouthWall(orientation) && (maze1[0][x-1]==18 || maze1[0][x-1]==17) && (maze2[mazeSize-y][x-1]==18 || maze2[mazeSize-y][x-1]==17)) {
            maze1[0][x] = 17; //West
            maze2[mazeSize-1-y][x] = 17; //East
         }
         else {
            maze1[0][x] = wallIndex; //West
            maze2[mazeSize-1][x] = wallIndex; //East
        }
        if (!northWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze1[i][e];
            }
          }
          maze[mazeSize-1][x] = 42; break;
        }
        else if (!southWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze2[i][e];
            }
          }
          maze[0][x] = 42; break;
        }
      }
      break;
    }
    case 2: {
      ////writeToServer2);
      maze1[0][0] = 18;
      maze2[0][mazeSize-1] = 18;
      while (!southWall) {
        moveSouth(orientation);
        wallIndex = getWallIndex(orientation);
        if (eastWall && checkWestWall(orientation) && (maze1[y-1][0]==18 || maze1[y-1][0]==17) && (maze2[y-1][mazeSize-1]==18 || maze2[y-1][mazeSize-1]==17)) {
            maze1[y][0] = 17; //West
            maze2[y][mazeSize-1] = 17; //East
         }
         else {
            maze1[y][0] = wallIndex; //West
            maze2[y][mazeSize-1] = wallIndex; //East
        }
        if (!eastWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze1[i][e];
            }
          }
          maze[y][0] = 42; break;
          }
        else if (!westWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze2[i][e];
            }
          }
          maze[y][mazeSize-1] = 42; break;
        }
      }
      break;
    }
    case 3: {
      ////writeToServer3);
      maze1[0][mazeSize-1] = 18;
      maze2[mazeSize-1][mazeSize-1] = 18;
      while (!westWall) {
        moveWest(orientation);
        wallIndex = getWallIndex(orientation);
        if (northWall && checkSouthWall(orientation) && (maze1[0][mazeSize-x]==18 || maze1[0][mazeSize-x]==17) && (maze2[mazeSize-1][mazeSize-x]==18 || maze2[mazeSize-1][mazeSize-x]==17)) {
            maze1[0][mazeSize-1-x] = 17; //West
            maze2[mazeSize-1][mazeSize-1-x] = 17; //East
         }
         else {
            maze1[0][mazeSize-1-x] = 17; //West
            maze2[mazeSize-1][mazeSize-1-x] = 17; //East
        }
        if (!northWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze1[i][e];
            }
          }
          maze[mazeSize-1][mazeSize-1-x] = 42; break;
        }
        else if (!southWall) {
          for (int i=0; i<mazeSize; i++) {
            for (int e=0; e<mazeSize; e++) {
              maze[i][e] = maze2[i][e];
            }
          }
          maze[0][mazeSize-1-x] = 42; break;
        }
      }
      break;
    }
  }*/
  while (!foundMiddle) {
    wallIndex = getWallIndex(orientation);
    //location[0] = findLocationY(maze, 42);
    //location[1] = findLocationX(maze, 42);
    int wallNumber = 4;
    northWall = checkNorthWall(orientation);
    eastWall = checkEastWall(orientation);
    southWall = checkSouthWall(orientation);
    westWall = checkWestWall(orientation);
    if (!northWall && maze[location[0]-1][location[1]]!=17) { wallNumber--; }
    if (!eastWall && maze[location[0]][location[1]+1]!=17) { wallNumber--; }
    if (!southWall && maze[location[0]+1][location[1]]!=17) { wallNumber--; }
    if (!westWall && maze[location[0]][location[1]-1]!=17) { wallNumber--; }
    switch (wallNumber) {
      case 3:
        if (!northWall) {
          //writeToServer0);
          goNorth();
        }
        else if (!eastWall) {
          //writeToServer1);
          goEast();
        }
        else if (!southWall) {
          //writeToServer2);
          goSouth();
        }
        else if (!westWall) {
          //writeToServer3);
          goWest();
        }
        break;
      case 2:
        if (!northWall && !eastWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]+1]!=16) {
            //writeToServer4);
            goNorth();
          }
          else if (maze[location[0]][location[1]+1]==16 && maze[location[0]-1][location[1]]!=16) {
            //writeToServer5);
            goEast();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
              //writeToServer6);
                goNorth();
                break;
              case 1:
              //writeToServer7);
                goEast();
                break;
            }
          }
        }
        else if (!northWall && !southWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]+1][location[1]]!=16) {
            //writeToServer8);
            goNorth();
          }
          else if (maze[location[0]+1][location[1]]==16 && maze[location[0]-1][location[1]]!=16) {
            //writeToServer9);
            goSouth();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
                //writeToServer10);
                goNorth();
                break;
              case 1:
                //writeToServer11);
                goSouth();
                break;
            }
          }
        }
        else if (!northWall && !westWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]-1]!=16) {
            //writeToServer12);
            goNorth();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]-1][location[1]]!=16) {
            //writeToServer13);
            goWest();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goWest();
                break;
            }
          }
        }
        else if (!eastWall && !southWall) {
          if (maze[location[0]][location[1]+1]==16 && maze[location[0]+1][location[1]]!=16) {
            goEast();
          }
          else if (maze[location[0]+1][location[1]]==16 && maze[location[0]][location[1]+1]!=16) {
            goSouth();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goSouth();
                break;
            }
          }
        }
        else if (!eastWall && !westWall) {
          if (maze[location[0]][location[1]+1]==16 && maze[location[0]][location[1]-1]!=16) {
            goEast();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]][location[1]+1]!=16) {
            goWest();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goWest();
                break;
            }
          }
        }
        else if (!southWall && !westWall) {
          if (maze[location[0]+1][location[1]]==16 && maze[location[0]][location[1]-1]!=16) {
            goSouth();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]+1][location[1]]!=16) {
            goWest();
          }
          else {
            switch (archiveDistance%2) {
              case 0:
                goSouth();
                break;
              case 1:
                goWest();
                break;
            }
          }
        }
        break;
      case 1:
        if (northWall) {
          if (maze[location[0]][location[1]+1]==16 && maze[location[0]+1][location[1]]!=16 && maze[location[0]][location[1]-1]!=16) {
            goEast();
          }
          else if (maze[location[0]+1][location[1]]==16 && maze[location[0]][location[1]+1]!=16 && maze[location[0]][location[1]-1]!=16) {
            goSouth();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]][location[1]+1]!=16 && maze[location[0]+1][location[1]]!=16) {
            goWest();
          
          else if (maze[location[0]][location[1]+1]!=16 && maze[location[0]+1][location[1]]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goSouth();
                break;
              case 1:
                goWest();
                break;
            }
          }
          else if (maze[location[0]+1][location[1]]!=16 && maze[location[0]][location[1]+1]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goWest();
                break;
            }
          }
          else if (maze[location[0]][location[1]-1]!=16 && maze[location[0]][location[1]+1]==16 && maze[location[0]+1][location[1]]==16) {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goSouth();
                break;
            }
          }
          else {
            switch (archiveDistance%3) {
              case 0:
                goEast();
                break;
              case 1:
                goSouth();
                break;
              case 2:
                goWest();
                break;
            }
          }
        }
        else if (eastWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]+1][location[1]]!=16 && maze[location[0]][location[1]-1]!=16) {
            goNorth();
          }
          else if (maze[location[0]+1][location[1]]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]-1]!=16) {
            goSouth();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]+1][location[1]]!=16) {
            goWest();
          }
          else if (maze[location[0]-1][location[1]]!=16 && maze[location[0]+1][location[1]]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goSouth();
                break;
              case 1:
                goWest();
            }
          }
          else if (maze[location[0]+1][location[1]]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goWest();
                break;
            }
          }
          else if (maze[location[0]][location[1]-1]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]+1][location[1]]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goSouth();
                break;
            }
          }
          else {
            switch (archiveDistance%3) {
              case 0:
                goNorth();
                break;
              case 1:
                goSouth();
                break;
              case 2:
                goWest();
                break;
            }
          }
        }
        else if (southWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]+1]!=16 && maze[location[0]][location[1]-1]!=16) {
            goNorth();
          }
          else if (maze[location[0]][location[1]+1]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]-1]!=16) {
            goEast();
          }
          else if (maze[location[0]][location[1]-1]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]+1]!=16) {
            goWest();
          }
          else if (maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]+1]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goWest();
                break;
            }
          }
          else if (maze[location[0]][location[1]+1]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]-1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goWest();
                break;
            }
          }
          else if (maze[location[0]][location[1]-1]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]+1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goEast();
                break;
            }
          }
          else {
            switch (archiveDistance%3) {
              case 0:
                goNorth();
                break;
              case 1:
                goEast();
                break;
              case 2:
                goWest();
                break;
            }
          }
        }
        else if (westWall) {
          if (maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]+1]!=16 && maze[location[0]+1][location[1]]!=16) {
            goNorth();
          }
          else if (maze[location[0]][location[1]+1]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]+1][location[1]]!=16) {
            goEast();
          }
          else if (maze[location[0]+1][location[1]]==16 && maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]+1]!=16) {
            goSouth();
          }
          else if (maze[location[0]-1][location[1]]!=16 && maze[location[0]][location[1]+1]==16 && maze[location[0]+1][location[1]]==16) {
            switch (archiveDistance%2) {
              case 0:
                goEast();
                break;
              case 1:
                goSouth();
                break;
            }
          }
          else if (maze[location[0]][location[1]+1]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]+1][location[1]]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goSouth();
                break;
            }
          }
          else if (maze[location[0]+1][location[1]]!=16 && maze[location[0]-1][location[1]]==16 && maze[location[0]][location[1]+1]==16) {
            switch (archiveDistance%2) {
              case 0:
                goNorth();
                break;
              case 1:
                goEast();
                break;
            }
          }
          else {
            switch (archiveDistance%3) {
              case 0:
                goNorth();
                break;
              case 1:
                goEast();
                break;
              case 2:
                goSouth();
                break;
            }
          }
        }
        break;
      default:
        if (maze[location[0]-1][location[1]]==16) {
          goNorth();
        }
        else if (maze[location[0]][location[1]+1]==16) {
          goEast();
        }
        else if (maze[location[0]+1][location[1]]==16) {
          goSouth();
        }
        else if (maze[location[0]][location[1]-1]==16) {
          goWest();
        }
        else {
          switch (archiveDistance%4) {
            case 0:
              goNorth();
              break;
            case 1:
              goEast();
              break;
            case 2:
              goSouth();
              break;
            case 3:
              goWest();
              break;
          }
        }
        break;
    }
  }
}
void loop() {}
