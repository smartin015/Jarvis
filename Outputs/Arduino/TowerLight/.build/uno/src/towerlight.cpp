#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
void setup();
void loop();
void init_manual();
void update_manual();
void init_party();
void update_party();
void init_off();
void update_off();
void init_light();
void update_light();
void init_sparkle();
void update_sparkle();
void init_chase();
void update_chase();
void init_triwipe();
void update_triwipe();
void init_rainbow();
void update_rainbow();
void init_rainbowchase();
void update_rainbowchase();
void init_flash();
void update_flash();
int new_fade_pos(int b);
void init_fade();
char fadefunc(char fade);
void update_fade();
uint32_t Wheel(byte WheelPos);
#line 1 "src/towerlight.ino"
//#include <Adafruit_NeoPixel.h>

#define LED 13
#define PIN 6
#define NLIGHTS 105
#define NRING 24
#define DEFAULT_STATE STATE_FADE
#define MANUAL_DROPOUT_MS 1000

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NLIGHTS+NRING, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

int dt = 30; // ms
byte j;
byte k;
bool on;

typedef enum State {
  STATE_OFF,
  STATE_LIGHT,
  STATE_FADE, 
  STATE_CHASE, 
  STATE_FLASH, 
  STATE_TRIWIPE, 
  STATE_RAINBOW,
  STATE_RAINBOWCHASE,
  STATE_PARTY, 
  STATE_MANUAL,
  NSTATES
};
State state = DEFAULT_STATE;

typedef void (* FuncPtr)();
const FuncPtr updaters[NSTATES] = {
  update_off, 
  update_light,
  update_fade, 
  update_chase, 
  update_flash, 
  update_triwipe,
  update_rainbow,
  update_rainbowchase,
  update_party,
  update_manual
};
const FuncPtr initializers[NSTATES] = {
  init_off,
  init_light, 
  init_fade, 
  init_chase, 
  init_flash, 
  init_triwipe,
  init_rainbow,
  init_rainbowchase,
  init_party,
  init_manual,
};

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

  Serial.begin(115200);
  Serial.print('A');
  initializers[state]();
}

void loop() {
  if (Serial.available() > 0) {
    state = (State)(Serial.read());
    if (state > NSTATES || state < 0) {
      state = STATE_OFF;
    }
    initializers[state]();
  }
  updaters[state]();
  strip.show();
  delay(dt);
}

void init_manual() {
  digitalWrite(LED, HIGH);
  // We want to stay in init until manual mode finishes.
  char IRGB[3];
  while (true) {
    //if (Serial.available() < 4) 
    //  continue;

    strip.setPixelColor(5, 255, 255, 255);
    strip.show();
    delay(50);

    while (Serial.available())
      Serial.read();

    /*
    Serial.readBytes(IRGB, 4);
    switch (IRGB[0]) {
      case char(0xff):
        strip.setPixelColor(5, 255, 255, 255);
        strip.show();
        continue;
      case char(0xfe):
        strip.setPixelColor(5, 0, 0, 255);
        strip.show();
        return;
      default:
        //strip.setPixelColor(IRGB[0], IRGB[1], IRGB[2], IRGB[3]);
        strip.setPixelColor(5, 0, 255, 0);
        strip.show();
        
    }*/
  }
  digitalWrite(LED, LOW);
}

void update_manual() {
  // Transition back to default state
  state = DEFAULT_STATE;
  initializers[DEFAULT_STATE]();
}


int substate;
int ctr;
#define PARTY_PD (NLIGHTS*3)
void init_party() {
  ctr = 0;
  substate = STATE_FADE+1;
  initializers[substate]();
}
void update_party() {
  updaters[substate]();
  ctr++;
  if (ctr == PARTY_PD) {
    ctr = 0;
    substate++;
    if (substate == STATE_PARTY) {
      substate == STATE_FADE+1;
    }
    initializers[substate]();
  }
}



void init_off() {}
void update_off() {
  for(int i=0; i < NLIGHTS; i++) {
    strip.setPixelColor(i, 0);
  }
}

void init_light() {
  for(int i=0; i < NLIGHTS; i++) {
    strip.setPixelColor(i, 120, 128, 128);
  }
}
void update_light() {
}

void init_sparkle() {
  dt = 30;
  j = 0;
  on = true;
}
void update_sparkle() {
  if (on) {
    for (int i=0; i < NLIGHTS; i=i+3) {
      strip.setPixelColor(i+j, 0, 0, 255);
    }
  } else {
    for (int i=0; i < NLIGHTS; i=i+3) {
      strip.setPixelColor(i+j, 0);
    }

    j++;
    if (j >= 3) {
      j = 0;
    }
  }
  on = !on;
}

void init_chase() {
  dt = 30;
  j = 0;
}
void update_chase() {
  for (int i=0; i < NLIGHTS; i=i+3) {
    strip.setPixelColor(i+j, 0);
  }

  j++;
  if (j >= 3) {
    j = 0;
  }

  for (int i=0; i < NLIGHTS; i=i+3) {
    strip.setPixelColor(i+j, 0, 0, 255);
  }
}

void init_triwipe() {
  dt = 15;
  j = 0;
  k = 0;
}
void update_triwipe() {
  switch(k) {
    case 0:
      strip.setPixelColor(j, 255, 0, 0);
      break;
    case 1:
      strip.setPixelColor(j, 0, 255, 0);
      break;
    case 2:
      strip.setPixelColor(j, 0, 0, 255);
      break;
  }
  j++;
  if (j > NLIGHTS) {
    j = 0;
    k = (k + 1) % 3;
  }
}

void init_rainbow() {
  dt = 30;
  j = 0; 
}
void update_rainbow() {
  for(int i=0; i<NLIGHTS; i++) {
    strip.setPixelColor(i, Wheel((i+j) & 255));
  }
  j++;
}

void init_rainbowchase() {
  dt = 30;
  j = 0;
  k = 0;
}
//Theatre-style crawling lights with rainbow effect
void update_rainbowchase() {
  for (int i=0; i < NLIGHTS; i=i+4) {
    strip.setPixelColor(i+k, 0);       
  }
  
  j++;
  k = (k + 1) % 4;

  for (int i=0; i < NLIGHTS; i=i+4) {
    strip.setPixelColor(i+k, Wheel( (i+j) % 255));    //turn every third pixel on
  }
}

void init_flash() {
  dt = 30;
  j = 60;
  on = true;
}
void update_flash() {
  // Flash from purple to reddish and back
  for(int i=0; i < NLIGHTS; i++) {
    strip.setPixelColor(i, j, 0, j);
  }

  if ((on && j > 235) || (!on && j < 80)) {
   on = !on;
  }

  if (on) {
    j = (j + 20); // Wraps around at 255
  } else {
    j = (j - 20);
  }

}


#define MAX_FADES 10
#define NBINS 4
#define FADELEN 60
#define BIN_L 31
#define BIN_W 22
typedef struct {
  char pos[MAX_FADES];
  char fade[MAX_FADES];
  char sz;
  char nfades;
  char strip_offs;
} Bin;
Bin bins[NBINS];

int new_fade_pos(int b) {
  while (true) {
    int newpos = bins[b].strip_offs + random(bins[b].sz);
    for (int i = 0; i < bins[b].nfades; i++) {
      if (newpos == bins[b].pos[i]) // Don't clobber existing fades
        continue;
    }
    return newpos;
  }
}

void init_fade() {
  dt = 55;
  on = true;

  randomSeed(analogRead(0));

  bins[0].sz = BIN_L;
  bins[0].strip_offs = 0;
  bins[0].nfades = 8;

  bins[1].sz = BIN_W;
  bins[1].strip_offs = BIN_L;
  bins[1].nfades = 5;

  bins[2].sz = BIN_L;
  bins[2].strip_offs = BIN_L+BIN_W;
  bins[2].nfades = 8;

  bins[3].sz = BIN_W - 1;
  bins[3].strip_offs = BIN_L+BIN_W+BIN_L;
  bins[3].nfades = 5;


  // Randomly init the fade cycle
  for(int b = 0; b < NBINS; b++) {
    for (int i = 0; i < bins[b].nfades; i++) {
      bins[b].pos[i] = -1;
    }

    for(int i = 0; i < bins[b].nfades; i++) {
      bins[b].fade[i] = random(-FADELEN, 0);
      bins[b].pos[i] = new_fade_pos(b);
    }
  }

  // And finally clear the strip
  for(int i=0; i < NLIGHTS; i++) {
    strip.setPixelColor(i, 0);
  }

}

char fadefunc(char fade) {
  if (fade > 30) {
    char newfade = 30 - 2*(fade-30);
    if (newfade < 0)
      return 0;
    return newfade;
  }
  return fade;
}

void update_fade() {
  for(int b=0; b < NBINS; b++) {
    for(int f=0; f < bins[b].nfades; f++) {
      char fade = bins[b].fade[f];

      if (fade > 0) {
        strip.setPixelColor(bins[b].pos[f], 0, 0, fadefunc(fade));
      }

      bins[b].fade[f]++;
      if (fade >= FADELEN) {
        bins[b].fade[f] = random(-FADELEN, 0);
        bins[b].pos[f] = new_fade_pos(b);
      }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}

