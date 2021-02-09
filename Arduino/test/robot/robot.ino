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
int dat;
void motorsPovorot(String d) {
  dat = d.toInt();
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor1.setSpeed(dat);
  motor2.setSpeed(dat);
}

void motorsSpeed(int motor1Speed, int motor2Speed) {
  motor1.setSpeed(motor1Speed);
  motor2.setSpeed(motor2Speed);
}

long times;
void setup() {
  // turn on motor
  Serial.begin(115200);
  motorsSpeed(100, 100);
  motorsRelease();
}
String data = "1";
void loop() {
  if (Serial.available() > 0) {
    data = Serial.readString();
    motorsPovorot(data);
    delay(10);
  }
}
