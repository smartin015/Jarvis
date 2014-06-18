#define AC_PIN 11

#define LED 13

void setup()
{
    Serial.begin(9600);
    pinMode(AC_PIN, OUTPUT);
    pinMode(LED, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    Serial.write(cmd);

    switch (cmd) {
      case 'T':
        digitalWrite(AC_PIN, HIGH);
        digitalWrite(LED, HIGH);
        break;
      case 'F':
        digitalWrite(AC_PIN, LOW);
        digitalWrite(LED, LOW);
        break;
      default:
        break;
    }
  }
  delay(50);
}
