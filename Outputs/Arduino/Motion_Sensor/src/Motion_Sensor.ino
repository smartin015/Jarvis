
#define LED_PIN 13
#define MOTION_PIN 12
#define LIGHT_POWER_PIN 2
#define LIGHT_PIN A0

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTION_PIN, INPUT);
  pinMode(LIGHT_POWER_PIN, OUTPUT);
  pinMode(LIGHT_PIN, INPUT);

  digitalWrite(LIGHT_POWER_PIN, HIGH);
}

byte last_state = 0;

void loop()
{
  delay(100);
  byte state = digitalRead(MOTION_PIN);

  if (last_state == state) {
    return;
  }

  int light = analogRead(LIGHT_PIN);

  // Signal is active low
  if (state == LOW) {
    Serial.print('0');
    Serial.print(' ');
    Serial.println(light);
  } else {
    Serial.print('1');
    Serial.print(' ');
    Serial.println(light);

  }
  last_state = state;
}   
