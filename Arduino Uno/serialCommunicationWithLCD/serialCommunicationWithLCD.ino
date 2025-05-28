# include <Wire.h>
# include "rgb_lcd.h"

rgb_lcd lcd;

const int soundSensor = A3;
const int threshold = 800; // 800 normal, 1000 for library environment

void setup() {
  pinMode(soundSensor, INPUT); // Sound sensor set as input
  lcd.begin(16, 2);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    if (data == "Computer Science") {
      lcd.clear();
      lcd.setCursor(4, 0);
      lcd.print("Computer");
      lcd.setCursor(4, 2);
      lcd.print("Science");
      delay(1000);
    }
    else if (data == "Marketing") {
      lcd.clear();
      lcd.setCursor(3, 0);
      lcd.print("Marketing");
      delay(1000);
    }
    else if (data == "Business"){
      lcd.clear();
      lcd.setCursor(4, 0);
      lcd.print("Business");
      delay(1000);
    }
  }

  int sensorValue = analogRead(soundSensor); // Read analog value from A3 pin
  int digitalValue = digitalRead(8); 
  //Serial.print("Analog: ");
  //Serial.print(sensorValue);
  //Serial.print(", Digital: ");
  //Serial.println(digitalValue);
  delay(1000);

  if(sensorValue > threshold){
    lcd.clear();
    lcd.setCursor(4, 0);
    lcd.print("Be Quiet");
    lcd.setCursor(4, 2);
    lcd.print("Too Loud");

    // Serial.println("This is the sound value:");
    // Serial.println(sensorValue);
    //Serial.println("Sound exceeds the threshold!");
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