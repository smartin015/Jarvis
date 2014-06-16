short incomingByte = 0;   // for incoming serial data
short startVar = 32766;
short stopVar = 32765;

//int arrLength = 200;
int flag = 200 + 1;
int temp[200];

int IRledPin =  4;    

boolean arr = false;
void setup() {
          pinMode(IRledPin, OUTPUT); 

        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        Serial.print('A');
}

void loop() {
  
    if (Serial.available() >= 2) {
      //incomingByte = Serial.read();
      incomingByte = word(Serial.read(),Serial.read());
      
      if(flag <= sizeof(temp))
     {
       temp[flag] = incomingByte;
       flag++;
     }
     
      //Serial.println(incomingByte);
      if (incomingByte == startVar)
      {
        Serial.println(incomingByte);
        flag = 0;
      }
      else if(incomingByte == stopVar)
      {
        flag = sizeof(temp) + 1;
        SendCode();
        Serial.print("\n");
      }
     
    }
   
}












// This procedure sends a 38KHz pulse to the IRledPin 
// for a certain # of microseconds. We'll use this whenever we need to send codes
void pulseIR(long microsecs) {
  // we'll count down from the number of microseconds we are told to wait
 
  cli();  // this turns off any background interrupts
 
  while (microsecs > 0) {
    // 38 kHz is about 13 microseconds high and 13 microseconds low
     
   digitalWrite(IRledPin, HIGH);  // this takes about 3 microseconds to happen
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
   digitalWrite(IRledPin, LOW);   // this also takes about 3 microseconds
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
 
   // so 26 microseconds altogether
   microsecs -= 26;
  }
 
  sei();  // this turns them back on
}
 
void SendCode() {
  
  //pulseIR(200000);
 
  for (int i = 0; i < sizeof(temp) - 1; i++){
   
    //Serial.println(temp[i]);
    //digitalWrite(IRledPin, HIGH);
    if (i%2 == 0) {
     
     pulseIR(temp[i]);
    }
    else
    {
    
      delayMicroseconds(temp[i]);
    }
    
  }
  Serial.println("DONE");
  
}
//python movement.py ProjectorScreenDown.txt
