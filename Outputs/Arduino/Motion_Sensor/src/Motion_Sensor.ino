
#define LED_PIN 13
#define MOTION_PIN 12

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTION_PIN, INPUT);
}

byte last_state = 0;

void loop()
{
  delay(100);
  byte state = digitalRead(MOTION_PIN);

  if (last_state == state) {
    return;
  }

  // Signal is active low
  if (state == LOW) {
    digitalWrite(LED_PIN, LOW);
    Serial.write(0);
  } else {
    digitalWrite(LED_PIN, HIGH);
    Serial.write(1);
  }
  last_state = state;
}   
