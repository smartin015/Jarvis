#define ID 0x01
#define ACTIVE_LOW 3

unsigned char RGB[3];
unsigned char currRGB[3];

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}

void init_RGB(const char* colmap) {
  for (int i = 0; i < 3; i++) {
    pinMode(colmap[i], OUTPUT);
    setPwmFrequency(colmap[i], 8); // Set to 3.9kHz
    analogWrite(colmap[i], (colmap[ACTIVE_LOW]) ? 255 : 0); 
  }
}

void write_RGB(const char* colmap) {
  for (int i = 0; i < 3; i++) {
    if (RGB[i] == currRGB[i]) continue;

    int val = (colmap[ACTIVE_LOW]) ? 255 - RGB[i] : RGB[i];
    analogWrite(colmap[i], val);
    currRGB[i] = RGB[i];
  } 
}

// For couch, 5 and 3 are switched, and active high
#define COUCH 1
#ifndef COUCH
const char RGB_MAP_1[] = {3, 5, 6, true};
#else
const char RGB_MAP_1[] = {5, 3, 6, false};
#endif
const char RGB_MAP_2[] = {9, 11, 10, true};

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);

  init_RGB(RGB_MAP_1);
  init_RGB(RGB_MAP_2);
}

int i = 0;
int strip = 0;
void loop()
{  
  while (Serial.available()) {
    char a = Serial.read();
    if (a == 0x01) {
      i = 0; 
      strip = 0;
      continue;
    } else if (strip > 1) {
      continue;
    }
    
    RGB[i] = a; i++;
    
    if (i == 3) {
      if (strip == 0)
          write_RGB(RGB_MAP_1);
      if (strip == 1)
          write_RGB(RGB_MAP_2);
      strip++;
      i = 0;
    }
  }
}
