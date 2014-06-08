#include <Arduino.h>

void setup();
void loop();
void pulseIR(long microsecs);
void SendCode();
#line 1 "src/IRBlaster.ino"
int incomingByte = 0;   // for incoming serial data
int startVar = 32766;
int stopVar = 32765;

int arrLength = 200;
int flag = arrLength + 1;
int temp[200];

#define IRledPin 4
#define LED 13

boolean arr = false;
void setup() {
  pinMode(IRledPin, OUTPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(IRledPin, LOW);
  digitalWrite(LED, LOW);
  Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
  Serial.print('X');
}

void loop() {
  if (Serial.available() >= 2) {

    byte lo = Serial.read();
    byte hi = Serial.read();
    incomingByte = word(hi, lo);
    Serial.write(lo);
    Serial.write(hi);
    
    if (incomingByte == startVar) {
      digitalWrite(LED, HIGH);
      flag = 0;
    }
    else if(incomingByte == stopVar) {
      digitalWrite(LED, LOW);
      SendCode(); 
    }
    else if (flag <= arrLength) {
      temp[flag] = incomingByte;
      flag++;
    }
    
  }
}

// This procedure sends a 38KHz pulse to the IRledPin 
// for a certain # of microseconds. We'll use this whenever we need to send codes
void pulseIR(long microsecs) {
  // we'll count down from the number of microseconds we are told to wait
 
  cli();  // this turns off any background interrupts
 
  while (microsecs > 0) {
    // 38 kHz is about 13 microseconds high and 13 microseconds low
     
   digitalWrite(IRledPin, HIGH);  // this takes about 3 microseconds to happen
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
   digitalWrite(IRledPin, LOW);   // this also takes about 3 microseconds
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
 
   // so 26 microseconds altogether
   microsecs -= 26;
  }
 
  sei();  // this turns them back on
}
 
void SendCode() {
  for (int i = 0; i < sizeof(temp) - 1; i++){
    if (i%2 == 0) {
      pulseIR((int)temp[i]);
    }
    else
    {
      delayMicroseconds((int)temp[i]);
    }
  }
  Serial.println("DONE");
}
