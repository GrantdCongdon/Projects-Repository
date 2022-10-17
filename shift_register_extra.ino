//This program controls a SN74HC595 IC shift register chip. The program controls 2 buttons that control the speed of the shift register.

// the next 6 lines of code define the pin numbers for the different pins on the shift register and buttons that the Arduino controls
int serial_input = 24;
int register_clock = 33;
int serial_clock = 29;
int button1 = 36;
int button2 = 30;
int button3 = 37;

int num_pins=16; // defines number of outputs the shift register(s) control
int count = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // begins Serial Communication
  // these 6 lines of code define the mode of each of the pins controlled by the Arduino
  pinMode(serial_input, OUTPUT);
  pinMode(register_clock, OUTPUT);
  pinMode(serial_clock, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
  
  digitalWrite(serial_input, LOW); // This line makes sets the serial input low for the future use of the pin

  reset(); // This line runs a custom function that resets all the outputs the shift register is controlling

}
// This function sets the value of the serial input High or Low depending on the input
int set(int x) {
  if (x==0) {
    digitalWrite(serial_input, LOW); // sets serial input high
  }
  else if (x==1) {
    digitalWrite(serial_input, HIGH); // sets Serial input low
  }
  else {
    Serial.println("Error"); // Writes to serial monitor that something is wrong
  }
}
// The next function shifts that value from the serail input to the first output pin
int shift(int rest_time) {
  digitalWrite(serial_clock, HIGH); // sets the pin high
  delay(rest_time); // waits for a defined time
  digitalWrite(serial_clock, LOW); // sets the pin low
}
// the function activate needs to be set high in order for the pin to allow the values to be displayed. This function 'activates' the pins
int activate(int rest_time) {
  digitalWrite(register_clock, HIGH); // sets register clock high
  delay(rest_time); // rests for a defined time
  digitalWrite(register_clock, LOW); // sets register clock low
}
// reset is the function run at the begining of the program that resets all the output pins
void reset() {
  for (int i=0; i<=num_pins; i++) {
    set(0);
    shift(50);
    
  }
  activate(50);
}
// This is the main function that is run in the program. It is the function that turns the lights on then off with rest time
int on_and_off(int rest_time, int pins) {
  for (int i = 0; i<pins; i++) { // this for loop runs until the number of pins is met by the variable i
    set(1); // sets the serial input pin High
    shift(rest_time); // shifts the value in
    activate(rest_time); // activates the output pin
  }
  for (int e = 0; e<pins; e++) {
    set(0); // sets the serial input pin Low
    shift(rest_time); // shifts the value in
    activate(rest_time); // activates the output pin
  }
}
int alternate(int rest_time, int pins) {
  int led_state=1; // defines a variable that is used to determine the led state
  int count = 0; // defines a counter used in a while loop later
  while (count<=pins) { // loops unil all pins that activated
    set(led_state); // sets serial input based on variable
    shift(rest_time); // shifts value in
    activate(rest_time); // activates ouput pins
    led_state++; // adds 1 to variable led_state
    if (led_state>=2) { // if led_state is greater than or equel to 2 then it resets the variable
      led_state=0;
    }
    count++; // adds one the counter variable
  }
  delay(2500);
  reset();
}
// creates a custom function used for customly seting values to be shifted in
int custom_set(int pins, int value1, int value2) {
  int value; // sets variable used to define the value of the serial input pin
  if (value1 == HIGH) { // if the first button is pressed set the variable that controls the serial input to 1
    value=1;
  }
  else if (value2 = HIGH) { // if the second button is pressed set that same variable to 0
    value=0;
  }
  set(value); // use the set function to set the serial input based on whatever button was pressed
  shift(50); // shift in the value
  activate(50); // refresh the board to display the new output
  count++; // increase the counter variable by 1
  if (count >= pins) { // check to see if all the pins have been given values
    delay(3000); // if true delay 3 seconds
    reset(); // and clear the board
  }
}
void loop() {
  // put your main code here, to run repeatedly:
  int value1 = digitalRead(button1); // checks to see if one of the two buttons is being pressed
  int value2 = digitalRead(button2); // checks the other button
  int value3 = digitalRead(button3); // checks the third button if it is being pressed
  if (value1==HIGH) { // if the first button is pressed ...
    on_and_off(50, num_pins); // run the main function
    delay(500); // wait half a second
  }
  else if (value2==HIGH) { // if the second button is pressed ...
    on_and_off(500, num_pins); // run the main loop except have a longer rest time
    delay(500); // wait half a second
  }
  else if (value3==HIGH) {
    alternate(100, num_pins);
    delay(500);
  }
  // loop back to the beggining of function
}

