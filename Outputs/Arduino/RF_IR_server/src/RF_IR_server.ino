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

char data[DATA_LEN];
char data_conf[DATA_LEN];

void setup(){
  Serial.begin(115200);
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
   
  Mirf.setRADDR((byte *)ADDY);
  Mirf.payload = DATA_LEN;
  Mirf.config();
}

void loop(){
  if (Serial.available() >= DATA_LEN) {
    Serial.readBytes(data, DATA_LEN);
    Mirf.setTADDR((byte *)"ctrl1");
    Mirf.send((byte *)data);

    while(Mirf.isSending()){}

    Serial.println("");
  }
}

