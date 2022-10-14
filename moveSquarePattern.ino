#include <Servo.h>
#include <stdio.h>
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
//sets variables for pulse 
Servo rightMotor;
Servo leftMotor;
SoftwareSerial mySerial(7, 6);
Adafruit_GPS GPS(&mySerial);
//counts the number of encoder inputs
volatile unsigned int encoderCountRight = 0;
volatile unsigned int encoderCountLeft = 0;
// Variables for pwm signal for both motors
int rightMotorPWM = 1300;
int leftMotorPWM = 1800;

void setup() {
  //Attach motors to pwm pins
  rightMotor.attach(11);
  leftMotor.attach(9);
  //Sets up the interrupt pins
  pinMode(3, INPUT);
  pinMode(2, INPUT);
  //One pin triggers whenever the encoder signal is rising from low to high and the other one triggers vice versa
  attachInterrupt(digitalPinToInterrupt(3), readEncoderRight, RISING);
  attachInterrupt(digitalPinToInterrupt(2), readEncoderLeft, FALLING);
  //Serial.begin(9600);
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  Serial.println("Adafruit GPS library basic test!");

  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz

  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  // the nice thing about this code is you can have a timer0 interrupt go off
  // every 1 millisecond, and read data from the GPS for you. that makes the
  // loop code a heck of a lot easier!
  useInterrupt(true);

  delay(1000);
  // Ask for firmware version
  mySerial.println(PMTK_Q_RELEASE);
}

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences. 
#define GPSECHO  false

// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;
void useInterrupt(boolean); // Func prototype keeps Arduino 0023 happy


// Interrupt is called once a millisecond, looks for any new GPS data, and stores it
SIGNAL(TIMER0_COMPA_vect) {
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
#ifdef UDR0
  if (GPSECHO)
    if (c) UDR0 = c;  
    // writing direct to UDR0 is much much faster than Serial.print 
    // but only one character can be written at a time. 
#endif
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
    usingInterrupt = true;
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
    usingInterrupt = false;
  }
}

uint32_t timer = millis();

double getGpsReadings(bool latitude) {
  //Create list of gps readings
  double gpsArray[2];
  // in case you are not using the interrupt above, you'll
  // need to 'hand query' the GPS, not suggested :(
  if (! usingInterrupt) {
    // read data from the GPS in the 'main loop'
    char c = GPS.read();
    // if you want to debug, this is a good time to do it!
    if (GPSECHO){
      if (c) Serial.print(c);
    }
  }
  
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences! 
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false
  
    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis())  timer = millis();

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) {
    timer = millis(); // reset the timer
    //Serial.print("Fix: "); Serial.print((int)GPS.fix);
    //Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
    if (GPS.fix) {
      Serial.print("Location: ");
      Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
      Serial.print(", ");
      Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);
      Serial.print("Location (in degrees, works with Google Maps): ");
      Serial.print(GPS.latitudeDegrees, 4);
      Serial.print(", ");
      Serial.println(GPS.longitudeDegrees, 4);
      gpsArray[0] = {GPS.latitudeDegrees};
      gpsArray[1] = {GPS.longitudeDegrees};
    }
  }
  if (latitude) {
    return gpsArray[0];
  }
  else {
    return gpsArray[1];
  }
}

void loop() {
  double latitude = getGpsReadings(true);
  double longitude = getGpsReadings(false);
  //Loops four times to go in a square or rectangle
  //loops while each encoder counter is less than 713 pulses which is 10 feet
  while (encoderCountRight <= 713 && encoderCountLeft <= 713) {
    //Calls function that sets PWM signals to both wheels
    moveBothMotors(rightMotorPWM, leftMotorPWM);
    //Calibrates the right motor if it is going faster than the left by counting the different in encoder counts
    if (encoderCountRight > encoderCountLeft) {
      /*Serial.println("Right");
      Serial.println(encoderCountRight);
      Serial.println(encoderCountLeft);
      Serial.println("Break");*/
      rightMotorPWM+=1;
      //Prevents overcorrection
      if (rightMotorPWM >= 1350) {
        rightMotorPWM-=2;
      }
    }
    //Calibrates the left motor is it is going faster than the right by counting the different in encoder counts
    else if (encoderCountLeft > encoderCountRight) {
      /*Serial.println("Left");
      Serial.println(encoderCountRight);
      Serial.println(encoderCountLeft);
      Serial.println("Break");*/
      leftMotorPWM-=1;
      //Prevents overcorrection
      if (leftMotorPWM <= 1675) {
        leftMotorPWM+=2;
      }
    }
    //Makes sure the computer isn't having to choose between greater than or less than so there is a perfect condition
    else {
      rightMotorPWM=rightMotorPWM;
      leftMotorPWM=leftMotorPWM;
    }
  }
  //Calls the function that stops both motors
  stopMotors();
  delay(500);
  //Resets the encoders for turning
  encoderCountRight = 0;
  encoderCountLeft = 0;
  //Sets PWM signals that the motors with use for turning
  rightMotorPWM=1300;
  leftMotorPWM=1800;
  //Runs both motors until each motor runs their amount around the circumference
  while (encoderCountRight <= 448 && encoderCountLeft <= 611) {
    moveBothMotors(rightMotorPWM, leftMotorPWM);
  }
  //Stops motors
  stopMotors();
  delay(500);
  //Resets the encoders and PWM signals for another run through so that the robot can go through a square
  encoderCountRight = 0;
  encoderCountLeft = 0;
  rightMotorPWM = 1250;
  leftMotorPWM = 1700;
  delay(500);
  //Makes sure than the program doesn't run again
  rightMotorPWM = 1000;
  leftMotorPWM = 1000;
  //Tries to exit the program
  exit(1);
}

void readEncoderRight() {
  encoderCountRight ++;
}
void readEncoderLeft() {
  encoderCountLeft++;
}
void moveBothMotors(int value1, int value2) {
  rightMotor.writeMicroseconds(value1);
  leftMotor.writeMicroseconds(value2);
  return 0;
}
void stopMotors() {
  rightMotor.writeMicroseconds(1500);
  leftMotor.writeMicroseconds(1500);
  return 0;
}

void accelerateBothMotors(int rightValue, int leftValue) {
  if (rightValue>1500 && leftValue<1500) {
    for (int i = 1500; i < rightValue; i+=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e > leftValue; e-=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue>1500 && leftValue>1500) {
    for (int i = 1500; i < rightValue; i+=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e < 1500; e+=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue<1500 && leftValue>1500) {
    for (int i = 1500; i > rightValue; i-=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 1500; e < 1500; e+=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  else if (rightValue<1500 && leftValue<1500) {
    for (int i = 0; i > rightValue; i-=2) {
      rightMotor.writeMicroseconds(i);
    }
    for (int e = 0; e > leftValue; e-=2) {
      leftMotor.writeMicroseconds(e);
    }
  }
  return 0;
}
