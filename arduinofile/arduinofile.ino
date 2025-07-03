#define motor1_en 10
#define motor2_en 11
#define motor1_dir1 4
#define motor1_dir2 5
#define motor2_dir1 6
#define motor2_dir2 7


char receivedChar;

void setup() {
  Serial.begin(9600); 
  Serial.println("Waiting for Bluetooth data...");
  
  for (unsigned int i = 4; i < 8; i++) {
    pinMode(i, OUTPUT);
  }

  pinMode(motor1_en, OUTPUT);
  pinMode(motor2_en, OUTPUT);
}

void Stop() {
  analogWrite(motor1_en, 0);
  analogWrite(motor2_en, 0);
  digitalWrite(motor1_dir1, LOW);
  digitalWrite(motor1_dir2, LOW);
  digitalWrite(motor2_dir1, LOW);
  digitalWrite(motor2_dir2, LOW);
}

void forward() {
  analogWrite(motor1_en, 120);
  analogWrite(motor2_en, 120);
  digitalWrite(motor1_dir1, HIGH);
  digitalWrite(motor1_dir2, LOW);
  digitalWrite(motor2_dir1, HIGH);
  digitalWrite(motor2_dir2, LOW);
  delay(2000);
  Stop();
  

}

void backward() {
  analogWrite(motor1_en, 120);
  analogWrite(motor2_en, 120);
  digitalWrite(motor1_dir1, LOW);
  digitalWrite(motor1_dir2, HIGH);
  digitalWrite(motor2_dir1, LOW);
  digitalWrite(motor2_dir2, HIGH);
  delay(2000);
  Stop();
}

void left() {
  analogWrite(motor1_en, 120);
  analogWrite(motor2_en, 120);
  digitalWrite(motor1_dir1, LOW);
  digitalWrite(motor1_dir2, HIGH);
  digitalWrite(motor2_dir1, HIGH);
  digitalWrite(motor2_dir2, LOW);
  delay(2000);
  analogWrite(motor1_en, 0);
  analogWrite(motor2_en, 0);
}

void right() {
  analogWrite(motor1_en, 120);
  analogWrite(motor2_en, 120);
  digitalWrite(motor1_dir1, HIGH);
  digitalWrite(motor1_dir2, LOW);
  digitalWrite(motor2_dir1, LOW);
  digitalWrite(motor2_dir2, HIGH);
  delay(2000);
  Stop();
  
}



void loop() {
  
  if (Serial.available()) {
    receivedChar = Serial.read();  
    Serial.print("Received: ");
    Serial.println(receivedChar);


    if (receivedChar == 'F') {
      Serial.println("Move Forward");
      forward();
    } else if (receivedChar == 'B') {
      Serial.println("Move Backward");
      backward();
    } else if (receivedChar == 'L') {
      Serial.println("Turn Left");
      left();
    } else if (receivedChar == 'R') {
      Serial.println("Turn Right");
      right();
    } else {
      Serial.println("Stop");
      Stop();
    }
  }
}

