/**
 * A Mirf example to test the latency between two Ardunio.
 *python movement.py projectorpower.txt
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
 * Note: To see best case latency comment out all Serial.println
 * statements not displaying the result and load 
 * 'ping_server_interupt' on the server.
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

short incomingByte = 0;   // for incoming serial data

byte irArray[100];
int arrLength = 100;
int flag = 0;

byte tempPin = 0;
byte tempVal = 0;

byte mirfData[16];


void setup(){
  Serial.begin(9600);
 
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  Mirf.setRADDR((byte *)"clie1");
  Mirf.payload = 16;
  Mirf.channel = 2;
  Mirf.config();
  
  Serial.print('A');
}

void loop(){
  
  if (Serial.available() > 0) {
      incomingByte = Serial.read();
      
      //checks if incoming byte matches an established ID
      //then runs appropriate command
      if (char(incomingByte) == char(CMD_IR)) {
        while(flag < arrLength) {
          if (Serial.available() > 0) {
            incomingByte = Serial.read();
            if(incomingByte == CMD_IR) {
              flag = arrLength;
              break;
            }
             
            irArray[flag] = incomingByte;
            flag++;
            Serial.print(flag);
          }
        }
        flag = 0;
        sendIRMirf();
        Serial.println("IR");
        Serial.print("\n");
      }
      else if (char(incomingByte) == char(CMD_ANALOG)) {
        while(flag < 2) {
          if (Serial.available() > 0) {
            incomingByte = Serial.read();
            
            if(flag == 0) {
              tempPin = incomingByte;
            } 
            else {
              tempVal = incomingByte;
            }
            flag++;
          }
        }
        sendAnalogMirf(tempPin, tempVal);
        flag = 0;
        tempPin = 0;
        tempVal = 0;
        Serial.println("send analog");
        Serial.print("\n");
      }
      else if (char(incomingByte) == char(CMD_DIGITAL)) {
        while(flag < 2) {
          if (Serial.available() > 0) {
            incomingByte = Serial.read();
            
            if(flag == 0) {
              tempPin = incomingByte;
            } 
            else {
              tempVal = incomingByte;
            }
            flag++;
          }
        }
        sendDigitalMirf(tempPin, tempVal);
        flag = 0;
        tempPin = 0;
        tempVal = 0;
        Serial.println("send dig");
        Serial.print("\n");
      }
      else if (char(incomingByte) == char(REQ_ANALOG)) {
        while(flag < 1) {
          if (Serial.available() > 0) {
            incomingByte = Serial.read();
            
            if(flag == 0) {
              tempPin = incomingByte;
            } 
            flag++;
          }
        }
        requestAnalogMirf(tempPin);
        flag = 0;
        tempPin = 0;
        Serial.println("req analog");
        Serial.print("\n");
      }
      else if (char(incomingByte) == char(REQ_DIGITAL)) {
        while(flag < 1) {
          if (Serial.available() > 0) {
            incomingByte = Serial.read();
            
            if(flag == 0) {
              tempPin = incomingByte;
            } 
            flag++;
          }
        }
        requestDigitalMirf(tempPin);
        flag = 0;
        tempPin = 0;
        Serial.println("reg dig");
        Serial.print("\n");
      }
      else {
        Serial.println("nope");
        Serial.print("\n");
      }
    }
 
  
} 

void sendDigitalMirf(byte pin, byte val) {
  Serial.print("Sending Digital");
   Mirf.setTADDR((byte *)"serv1");
   
   byte sendingData[] = {CMD_DIGITAL, pin, val};
   
   Mirf.send(sendingData);
   
   while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
  
}

void sendAnalogMirf(byte pin, byte val) {
  Serial.print("Sending Analog");
   Mirf.setTADDR((byte *)"serv1");
   
   byte sendingData[16] = {CMD_ANALOG, pin, val};
   
   Mirf.send(sendingData);
   
   while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
  
}
  
void sendIRMirf() {
  //Serial.print("Sending IR");
  Mirf.setTADDR((byte *)"serv1");
  
  byte sendingData[16] = {CMD_IR, 7};
  
  Mirf.send(sendingData);
  
   while(Mirf.isSending()){
  }
  delay(500);
  
   for(int i = 0; i < 100; i+=15) {
     sendingData[15] = (i/15);
      for(int j = 0; j < 15; j++) {
          sendingData[j] = irArray[i+j];
          Serial.print(irArray[i+j]);
      }
      //Serial.print("\nSending byte arr with #'s: ");
      for(int i = 0; i < 16; i++) {
        //Serial.print(sendingData[i]);
        //Serial.print(" ");
      }
      //Serial.println(irArray[i]);
      Mirf.send(sendingData);
          while(Mirf.isSending()){}
          delay(100);
   }
}









void requestAnalogMirf(byte pin) {
  Serial.print("Requesting Analog");
   Mirf.setTADDR((byte *)"serv1");
   
   byte sendingData[16] = {REQ_ANALOG, pin};
   
   Mirf.send(sendingData);
   
   while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
  
  boolean requestSentinel = true;
  
  while (requestSentinel) {
    
    while(Mirf.dataReady()) {
      Mirf.getData(mirfData);
      if(mirfData[0] = SNT_ANALOG) {
        
        Serial.print("Data received: ");
        Serial.println(mirfData[1]);
        requestSentinel = false;
      }
      
    }
    
  }
}

void requestDigitalMirf(byte pin) {
  Serial.print("Requesting Digital");
  
   Mirf.setTADDR((byte *)"serv1");
   
   byte sendingData[16] = {REQ_DIGITAL, pin};
   
   Mirf.send(sendingData);
   
   while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
  
  boolean requestSentinel = true;
  
  while (requestSentinel) {
    
    while(Mirf.dataReady()) {
      Mirf.getData(mirfData);
      if(mirfData[0] = SNT_DIGITAL) {
        
        Serial.print("Data received: ");
        Serial.println(mirfData[1]);
        requestSentinel = false;
      }
      
    }
    
  }
}


