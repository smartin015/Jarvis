/**
 * A Mirf example to test the latency between two Ardunio.
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
 * Note: To see best case latency comment out all Serial.println
 * statements not displaying the result and load 
 * 'ping_server_interupt' on the server.<
 */

#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>
#include "commands.h"

#define ADDY "serv1"

#define SERIAL_LEN 5
char data[SERIAL_LEN+1];

void setup(){
  Serial.begin(115200);
  
  data[SERIAL_LEN] = '\0';

  Mirf.spi = &MirfHardwareSpi; //new MirfSpiDriver();//&MirfHardwareSpi;
  Mirf.init();
   
  Mirf.setRADDR((byte *)ADDY);
  Mirf.payload = DATA_LEN;
  Mirf.config();
  Serial.println("Ready");
}

void loop(){
  if (Serial.available() >= SERIAL_LEN) {
    Serial.readBytes(data, SERIAL_LEN);
    if (data[DATA_LEN]) {
      // If we have more than DATA_LEN in data, 
      // we must be trying to set TADDR
      Mirf.setTADDR((byte *)data);
      Serial.print("SET TARGET TO ");
      Serial.println(data);
      for (int i = 0; i < SERIAL_LEN; i++) {
        data[i] = 0;
      }
    } else {
      Mirf.send((byte *)data);
      while(Mirf.isSending()){}
    }
    Serial.println("");
  }
}

