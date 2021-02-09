#include <AFMotor.h>
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

int i;
int t;

void motorsRelease() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);  
}

void motorsForward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);  
  motor1.setSpeed(255);
  motor2.setSpeed(255);
}

void motorsBackward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD); 
  motor1.setSpeed(255);
  motor2.setSpeed(255); 
}

void motorsPovorot(int angle){
  Serial.println(angle);
  float t_360 = 1700.0;
  t = (int)((t_360 * angle) / 360);
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  Serial.println(t);
  delay(t);
}

void motorsSpeed(int motor1Speed, int motor2Speed) {
  motor1.setSpeed(motor1Speed);
  motor2.setSpeed(motor2Speed);
}

void setup() {
  // turn on motor
  Serial.begin(115200);
  motorsSpeed(100, 100);
  motorsRelease();
}

void loop() {  
    motorsPovorot(90);
    motorsRelease();
    delay(1000);
    if(Serial.available()>0) {
    String data = Serial.readString();
    if (data ){
      motorsForward();
      delay(2000);
    }
      motorsRelease();
      delay(1000);
    if (data == "-1"){
      motorsBackward();
      delay(2000);
    }
      motorsRelease();
      delay(1000);
    }
}