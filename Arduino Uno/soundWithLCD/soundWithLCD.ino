# include <Wire.h>
# include "rgb_lcd.h"

rgb_lcd lcd;

const int soundSensor = A3;
const int threshold = 800; // 800 normal, 1000 for library environment

void setup() {
  pinMode(soundSensor, INPUT); // Sound sensor set as input
  lcd.begin(16, 2);

  Serial.begin(9600); // Start serial communication at 9600 bps
}

void loop() {
  int sensorValue = analogRead(soundSensor); // Read analog value from A3 pin
  int digitalValue = digitalRead(8); 
  Serial.print("Analog: ");
  Serial.print(sensorValue);
  Serial.print(", Digital: ");
  Serial.println(digitalValue);
  delay(1000);

  if(sensorValue > threshold){
    lcd.clear();
    lcd.setCursor(4, 0);
    lcd.print("Be Quiet");
    lcd.setCursor(4, 2);
    lcd.print("Too Loud");

    // Serial.println("This is the sound value:");
    // Serial.println(sensorValue);
    Serial.println("Sound exceeds the threshold!");
    // Serial.println();
    delay(1000);
  }
  else{
    lcd.clear();
    lcd.setCursor(6, 0);
    lcd.print("o  o");
    lcd.setCursor(5, 1);
    lcd.print("[____]");
    delay(100);
  }
}