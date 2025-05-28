const int EM1 = 6;  
const int EM2 = 7;  

void setup() {
  pinMode(EM1, OUTPUT);
  pinMode(EM2, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  digitalWrite(EM1, HIGH); 
  digitalWrite(EM2, HIGH);
  delay(10000);
  digitalWrite(EM1, LOW);  
  digitalWrite(EM2, LOW); 
  delay(5000);
}