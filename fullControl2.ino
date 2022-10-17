#include <Servo.h>
#include <Adafruit_MAX31856.h>
Servo conveyor; //Pin 3
Servo door; //Pin 5
Servo dispensor; //Pin 6
const int midpoint = 1510;
const int conveyorPWM = 1250;
const int leftTransistor = 24;
const int rightTransistor = 34;
const int stopSwitch = 28;
int upperState, lowerState, stopState;
Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(8, 10, 6, 12);
int fTemp;
void setup() {
  //Setup pins and other devices
  Serial.begin(9600); maxthermo.begin();
  conveyor.attach(2); door.attach(5); dispensor.attach(6);
  pinMode(upperButton, INPUT); pinMode(lowerButton, INPUT);
  pinMode(rightTransistor, OUTPUT); pinMode(leftTransistor, OUTPUT);
  pinMode(stopSwitch, INPUT);
  maxthermo.setThermocoupleType(MAX31856_TCTYPE_K);
  stopConveyor(); countDown(3, 1);
  //Start the devices and other controls
  fTemp = maxthermo.readThermocoupleTemperature();
  fTemp = (fTemp * 1.8) + 32;
  openDoor();
  delay(500);
  stopState = digitalRead(stopSwitch);
  while (stopState == LOW) {
    moveConeyor(conveyorPWM);
    stopState = digitalRead(stopSwitch);
    delay(1);
  }
  stopConveyor(); closeDoor();
  while (fTemp < 350) {
    digitalWrite(leftTransistor, HIGH);
    fTemp = maxthermo.readThermocoupleTemperature();
    fTemp = (fTemp * 1.8) + 32;
    Serial.println(fTemp);
  }
  dispenseCookies(x, y, z);
  openDoor();
  delay(500);
  moveConveyor(conveyorPWM);
  digitalWrite(leftTransistor, LOW);
}

void loop() {
  upperState = digitalRead(upperButton);
  lowerState = digitalRead(lowerButton);
  stopState = digitalRead(stopSwitch);
  fTemp = maxthermo.readThermocoupleTemperature();
  fTemp = (fTemp * 1.8) + 32;
  if (fTemp >= 352) {
    digitalWrite(leftTransistor, LOW);
  }
  else {
    digitalWrite(leftTransistor, HIGH);
  }
  openDoor();
  delay(500);
  moveConveyor(conveyorPWM);
  if (stopState == HIGH) {
    stopConveyor(); closeDoor();
    cook();
    openDoor();
    dispenseCookies();
    moveConveyor(conveyorPWM);
  }
}

void countDown(int iterations, int t) {
  Serial.print("Starting in ");
  for (int i=0; i < iterations; i++) {
    Serial.println(iterations-i);
    delay(t*1000);
  }
  Serial.println("Start");
}
void moveConveyor(int value) {
  conveyor.writeMicroseconds(value);
}
void stopConveyor() {
  conveyor.writeMicroseconds(midpoint);
}
void openDoor() {
  door.writeMicroseconds(1000);
}
void closeDoor() {
  door.writeMicroseconds(2200);
}
void dispenseCookies(int x, int y, int z) {
  dispensor.writeMicroseconds(x); delay(y);
  moveConveyor(conveyorPWM); delay(z);
  dispensor.writeMicroseconds(x); delay(y);
  moveConveyor(conveyorPWM); delay(z);
  dispensor.writeMicroseconds(x); delay(y);
}
void cook() {
  for (int i = 0; i < 660; i++) {
    fTemp = maxthermo.readThermocoupleTemperature();
    fTemp = (fTemp * 1.8) + 32;
    if (fTemp >= 352) {
      digitalWrite(leftTransistor, LOW);
    }
    else {
      digitalWrite(leftTransistor, HIGH);
    }
    Serial.print(fTemp);
    delay(1000);
  }
}
