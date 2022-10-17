#include <Adafruit_MAX31856.h>
const int leftTransistor = 24;
const int upperButton = 44;
const int rightTransistor = 34;
const int lowerButton = 50;
const int stopSwitch = 28;
int upperState, lowerState, stopState;
Adafruit_MAX31856 maxthermo = Adafruit_MAX31856(8, 10, 6, 12);
void setup() {
  maxthermo.begin();
  Serial.begin(115200);
  maxthermo.setThermocoupleType(MAX31856_TCTYPE_K);
  pinMode(upperButton, INPUT);
  pinMode(lowerButton, INPUT);
  pinMode(rightTransistor, OUTPUT);
  pinMode(leftTransistor, OUTPUT);
  pinMode(stopSwitch, INPUT);
  countDown(3, 1);

}

void loop() {
  upperState = digitalRead(upperButton);
  lowerState = digitalRead(lowerButton);
  stopState = digitalRead(stopSwitch);
  int fTemp = maxthermo.readThermocoupleTemperature();
  fTemp = (fTemp * 1.8) + 32;
  if (upperState == HIGH) {
    digitalWrite(rightTransistor, HIGH);
  }
  else {
    digitalWrite(rightTransistor, LOW);
  }
  if (lowerState == HIGH) {
    digitalWrite(leftTransistor, HIGH);
  }
  else {
    digitalWrite(leftTransistor, LOW);
  }
  if (fTemp >= 352) {
    digitalWrite(leftTransistor, LOW);
  }
  else {
    digitalWrite(leftTransistor, HIGH);
  }
  uint8_t fault = maxthermo.readFault();
  if (fault) {
    if (fault & MAX31856_FAULT_CJRANGE) Serial.println("Cold Junction Range Fault");
    if (fault & MAX31856_FAULT_TCRANGE) Serial.println("Thermocouple Range Fault");
    if (fault & MAX31856_FAULT_CJHIGH)  Serial.println("Cold Junction High Fault");
    if (fault & MAX31856_FAULT_CJLOW)   Serial.println("Cold Junction Low Fault");
    if (fault & MAX31856_FAULT_TCHIGH)  Serial.println("Thermocouple High Fault");
    if (fault & MAX31856_FAULT_TCLOW)   Serial.println("Thermocouple Low Fault");
    if (fault & MAX31856_FAULT_OVUV)    Serial.println("Over/Under Voltage Fault");
    if (fault & MAX31856_FAULT_OPEN)    Serial.println("Thermocouple Open Fault");
  }
  Serial.println(fTemp);
}
void countDown(int iterations, int t) {
  Serial.print("Starting in ");
  for (int i=0; i < iterations; i++) {
    Serial.println(iterations-i);
    delay(t*1000);
  }
  Serial.println("Start");
}
