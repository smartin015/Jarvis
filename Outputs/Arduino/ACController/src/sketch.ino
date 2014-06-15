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
    Serial.write(cmd);
    switch (cmd) {
      case 'T':
        digitalWrite(AC_PIN, HIGH);
        break;
      case 'F':
        digitalWrite(AC_PIN, LOW);
        break;
      default:
        break;
    }
  }
  delay(50);
}
