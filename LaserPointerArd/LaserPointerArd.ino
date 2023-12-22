#include <Servo.h>
Servo servoX;
Servo servoY;
int x;
int y;
void setup() {
  Serial.begin(28800);
  servoX.attach(10);
  servoY.attach(3);

}

void loop() {
 if(Serial.available()>=2){
  x = Serial.read();
  y = Serial.read();
  servoX.write(x); 
  servoY.write(y);
 }
}
