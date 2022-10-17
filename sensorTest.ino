#define frontDistance A3
#define backDistance A1
#define rightDistance A2
#define leftDistance A0
const int frontWallCorrection = 775;
const int backWallCorrection = 775;
int correctFront() {
  int frontWallDistance;
  int fD1=0, fD2=0, fD3=0;
  delay(10);
  while (fD1<400 || fD1>2000) { fD1 = analogRead(frontDistance); }
  while (fD2<400 || fD2>2000) { fD2 = analogRead(frontDistance); }
  while (fD3<400 || fD3>2000) { fD3 = analogRead(frontDistance); }
  if (fD1 > fD2 && fD1 > fD3) { frontWallDistance = fD1; }
  else if (fD2 > fD1 && fD2 > fD3) { frontWallDistance = fD2; }
  else { frontWallDistance = fD3; }
  if (frontWallDistance>frontWallCorrection) { return 1; }
  else { return 0; }
}
int correctBack() {
  int backWallDistance;
  int bD1=0, bD2=0, bD3=0;
  delay(10);
  while (bD1<400 || bD1>2000) { bD1 = analogRead(backDistance); }
  while (bD2<400 || bD2>2000) { bD2 = analogRead(backDistance); }
  while (bD3<400 || bD3>2000) { bD3 = analogRead(backDistance); }
  if (bD1 > bD2 && bD1 > bD3) { backWallDistance = bD1; }
  else if (bD2 > bD1 && bD2 > bD3) { backWallDistance = bD2; }
  else { backWallDistance = bD3; }
  if (backWallDistance>backWallCorrection) { return 1; }
  else { return 0; }
}
int getRightDistance() {
  int rightWallDistance;
  int rD1=0, rD2=0, rD3=0;
  delay(50);
  while (rD1<400 || rD1>2000) { rD1 = analogRead(rightDistance); }
  while (rD2<400 || rD2>2000) { rD2 = analogRead(rightDistance); }
  while (rD3<400 || rD3>2000) { rD3 = analogRead(rightDistance); }
  if (rD1 > rD2 && rD1 > rD3) { rightWallDistance = rD1; }
  else if (rD2 > rD1 && rD2 > rD3) { rightWallDistance = rD2; }
  else { rightWallDistance = rD3; }
  Serial.println(rightWallDistance);
  //double actualDistance = (0.0002*(rightWallDistance*rightWallDistance))-(0.3249*rightWallDistance)+143.59;
  return rightWallDistance;
}
//Max is 11.5
//Min is 28
double getLeftDistance() {
  double leftWallDistance;
  int lD1=0, lD2=0, lD3=0;
  delay(50);
  while (lD1<400 || lD1>2000) { lD1 = analogRead(leftDistance); }
  while (lD2<400 || lD2>2000) { lD2 = analogRead(leftDistance); }
  while (lD3<400 || lD3>2000) { lD3 = analogRead(leftDistance); }
  if (lD1 > lD2 && lD1 > lD3) { leftWallDistance = lD1; }
  else if (lD2 > lD1 && lD2 > lD3) { leftWallDistance = lD2; }
  else { leftWallDistance = lD3; }
  //double actualDistance = (0.0002*(leftWallDistance*leftWallDistance))-(0.3013*leftWallDistance)+136.06;
  return leftWallDistance;
}
//Min of 22
//Max of 32
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println(getRightDistance());

}
