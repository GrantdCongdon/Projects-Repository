
int serial_input = 24;
int register_clock = 33;
int serial_clock = 29;
int version_button1 = 36;
int button2 = 30;

int num_pins=16;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(serial_input, OUTPUT);
  pinMode(register_clock, OUTPUT);
  pinMode(serial_clock, OUTPUT);
  pinMode(version_button1, INPUT);
  pinMode(button2, INPUT);
  
  digitalWrite(serial_input, LOW);
  Serial.begin(9600);

  reset();

}

int set(int x) {
  if (x==0) {
    digitalWrite(serial_input, LOW);
  }
  else if (x==1) {
    digitalWrite(serial_input, HIGH);
  }
  else {
    Serial.println("Error");
  }
}

int shift(int rest_time) {
  digitalWrite(serial_clock, HIGH);
  delay(rest_time);
  digitalWrite(serial_clock, LOW);
}

int activate(int rest_time) {
  digitalWrite(register_clock, HIGH);
  delay(rest_time);
  digitalWrite(register_clock, LOW);
}

void reset() {
  for (int i=0; i<=num_pins; i++) {
    set(0);
    shift(50);
    
  }
  activate(50);
}

int on_and_off(int rest_time, int pins) {
  Serial.println("Started\n");
  for (int i = 0; i<pins; i++) {
    set(1);
    shift(rest_time);
    activate(rest_time);
  }
  for (int e = 0; e<pins; e++) {
    set(0);
    shift(rest_time);
    activate(rest_time);
  }
  Serial.println("Ended Second loop\n");
}

void loop() {
  // put your main code here, to run repeatedly:
  int value1 = digitalRead(version_button1);
  int value2 = digitalRead(button2);
  if (value1==HIGH) {
    Serial.println("Started");
    on_and_off(50, num_pins);
    delay(500);
  }
  else if (value2==HIGH) {
    on_and_off(500, num_pins);
    delay(500);
  }
}
