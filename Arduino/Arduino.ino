#include <AFMotor.h>
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

int i;
int motors[] = {0, 0, 0, 0};
int motorNumber = 0;
bool isCommandDetected = false;

void motorsRelease() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);  
}

void motorsForward() {
  motor1.run(FORWARD);
  motor2.run(FORWARD);  
}

void motorsBackward() {
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);  
}

void motorsLeft() {
  motor1.run(BACKWARD);
  motor2.run(FORWARD);  
}

void motorsRight() {
  motor1.run(FORWARD);
  motor2.run(BACKWARD);  
}

void motorsSpeed(int motor1Speed, int motor2Speed) {
  motor1.setSpeed(motor1Speed);
  motor2.setSpeed(motor2Speed);
}

void setup() {
  Serial.begin(9600);
  // turn on motor
  motorsSpeed(100, 100);
  motorsRelease();
}

void loop() {
  if (Serial.available()>0) {
    isCommandDetected = true;
    int data = Serial.read();
    if (motorNumber < 2) {
      motors[motorNumber] = data;
      motorNumber++;
    }
    else {
      if(motorNumber == 3)
      {
        motors[3] = data;
      }
      else{
        motors[2] = data;
        motorNumber++;
      }
    }
  } else {
    if (isCommandDetected) {      
      isCommandDetected = false;
      motorNumber = 0;
    }
  }

  if (motors[0] == 0 && motors[1] == 0 && motors[2] == 1 && motors[3] == 1) {
    motorsRelease();
  } else {
    if(motors[2] == 1)
    {
      motorsLeft();
      motorsSpeed(motors[0], motors[1]);
    }
    else
    {
      if(motors[3] == 1)
      {
        motorsRight();
        motorsSpeed(motors[0], motors[1]);
      }
      else
      {
        motorsForward();
        motorsSpeed(motors[0], motors[1]);
      }
    }
  }
//  delay(10);
}
