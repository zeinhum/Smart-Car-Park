#include <Servo.h>

Servo myservo;  // create servo object to control a servo
const int servoPin = 10; // Servo signal pin
const int echoPin = 8; //ultrasonic sensor pin
const int trigPin = 9;

//operate ultrasonic sensor/ parking spot


void detectObject(float objDistance){
  digitalWrite(trigPin, LOW);
  delay(5);
  digitalWrite(trigPin, HIGH);
  delay(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = duration*0.034/2;
  
  if(distance <= objDistance){
    Serial.println("occupied");
    
  } else{
    Serial.println("available");
    
  }
}

// operate servomotor/ gate
void controlGate() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "open") {
      for (int i = 0; i <= 80; i++) {
        myservo.write(i);
        delay(20);
      }
      delay(7000);
      for(int i = 80; i>=0; i--){
        myservo.write(i);
        delay(20);
      }
      
      Serial.println("Gate closed"); // Add this line
    }
  }
}




void setup() {
  myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  myservo.write(0); // Initialize servo to closed position (0 degrees)

  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
}

void loop() {
  detectObject(7);
  delay(100);
  controlGate();
  delay(100);
}