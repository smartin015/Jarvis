/**
 * An Mirf example which copies back the data it recives.
 *
 * Pins:
 * Hardware SPI:
 * MISO -> 12
 * MOSI -> 11
 * SCK -> 13
 *
 * Configurable:
 * CE -> 8
 * CSN -> 7
 *
 */

#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

#define CMD_IR 231

#define CMD_ANALOG 241
#define REQ_ANALOG 242
#define SNT_ANALOG 243

#define CMD_DIGITAL 251
#define REQ_DIGITAL 252
#define SNT_DIGITAL 253

int IRledPin =  4;

int payload = 16;
//int finalArrSentinel = 0;
int sentinel = 0;
int numIRBytes = 0;

#define arrLength 112
int finalIntArr[arrLength];
byte data[16];
//byte packetIDArr[10];

void setup(){
  Serial.begin(9600);
  pinMode(IRledPin, OUTPUT); 
  /*
   * Set the SPI Driver.
   */

  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  Mirf.setRADDR((byte *)"serv1");
  Mirf.payload = payload;
  Mirf.channel = 2;
  Mirf.config();
  Serial.println("Listening..."); 
  
}

void loop(){
  //digitalWrite(IRledPin, HIGH);
     //loop starts when there is data availablee
     
     while(Mirf.dataReady()) {
       /*first step is to check if this data is part
       an IR command. 
       if numirbytes equals zero, then an ir code is not
       expected
       */
       if(numIRBytes == 0) {
         Mirf.getData(data);
          
         //checks if ir, analog, or digital. keeps numbytes 0 if not an ir command
         numIRBytes = processData();
       }
       /*if numirbytes != 0 and sentinel is < numirbytes,
        then the data is part of an ir code, and is appended to
        the ir array
        */
       else if (sentinel < numIRBytes)
       {
         Mirf.getData(data);
         
         //Serial.print("Packet ID#: ");
         //Serial.println(data[15]);
         
         for (int i = 0; i < 15; i++) {
           //finalArrSentinel++;
           //finalIntArr[sentinel*15+i] = int(data[i])*10;  
           finalIntArr[0] = 5;   
         }
         //packetIDArr[sentinel] = data[15];
      
         sentinel++;
         if(sentinel == 7) {
         sendIRCommand();
         }
       }
       /*if numirbytes != 0 and sentinel is >= numirbytes,
       then the end of the ir code has been reached, so
       reset sentinel, numirbytes, and sendIRcommand
        */
       else {
         //sendIRCommand();
         sentinel = 0;
         numIRBytes = 0;
         //finalArrSentinel = 0;
       }
       
     }
      delay(50);
     
 
}

int processData() {
  if(data[0] == CMD_ANALOG) {
    Serial.println("Analog packet");
    analogCommand(data[1], data[2]);
    return 0;
  }
  else if(data[0] == CMD_DIGITAL) {
    Serial.println("Digital packet");
    digitalCommand(data[1], data[2]);
    return 0;
  }
  else if(data[0] == REQ_ANALOG) {
    Serial.println("Analog request");
    analogRequest(data[1]);
    return 0;
  }
  else if(data[0] == REQ_DIGITAL) {
    Serial.println("Digital request");
    digitalRequest(data[1]);
    return 0;
  }
  else if(data[0] == CMD_IR) {
    Serial.print("IR: len ");
    Serial.println(data[1]);
    return data[1];
  }
  else {
    Serial.println("unexpected packet");
    return 0;
  }
  return 0;
}

void analogCommand(byte pin, byte val) {
  pinMode(pin, OUTPUT);
  analogWrite(pin, val);
  
  if(pin = 0) {
    pinMode(A0, OUTPUT);
    analogWrite(A0, val);
  } else if(pin = 1) {
    pinMode(A1, OUTPUT);
   analogWrite(A1, val);
  } else if(pin = 2) {
    pinMode(A2, OUTPUT);
    analogWrite(A2, val);
  } else if(pin = 3) {
    pinMode(A3, OUTPUT);
    analogWrite(A3, val);
  } else if(pin = 4) {
    pinMode(A4, OUTPUT);
    analogWrite(A4, val);
  } else if(pin = 5) {
    pinMode(A5, OUTPUT);
    analogWrite(A5, val);
  } else if(pin = 6) {
    pinMode(A6, OUTPUT);
    analogWrite(A6, val);
  } else if(pin = 7) {
    pinMode(A7, OUTPUT);
    analogWrite(A7, val);
  }
  
  Serial.print("pin: ");
  Serial.println(pin);
  Serial.print("val: ");
  Serial.println(val);
}

void digitalCommand(byte pin, byte val) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, val);
  Serial.print("pin: ");
  Serial.println(pin);
  Serial.print("val: ");
  Serial.println(val);
}

const byte ANALOG[] = {A0, A1, A2, A3, A4, A5, A6, A7};
void analogRequest(byte pin) {
  pinMode(ANALOG[pin], INPUT);
  data[1] = analogRead(ANALOG[pin]);
  data[0] = SNT_ANALOG;
  Mirf.send(data);
  while(Mirf.isSending()){}
}

void digitalRequest(byte pin) {
  pinMode(pin, INPUT);
  data[0] = SNT_DIGITAL;
  data[1] = digitalRead(pin);
  Mirf.send(data);
  while(Mirf.isSending()){}
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
 
void sendIRCommand() {
  for (int i = 0; i < arrLength; i++){
    if (i%2 == 0) {
      pulseIR(finalIntArr[i]);
    }
    else {
      delayMicroseconds(finalIntArr[i]);
    } 
  }
  //Serial.println("DONE");
}
