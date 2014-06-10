#define AC_PIN 12

void setup()
{
    Serial.begin(9600);
    pinMode(AC_PIN, OUTPUT);
}

void loop()
{
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    switch (cmd) {
      case 'T':
        pinMode(AC_PIN, HIGH);
        break;
      case 'F':
        pinMode(AC_PIN, LOW);
        break;
      default:
        break;
    }
  }
  delay(50);
}
