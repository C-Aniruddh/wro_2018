//(in22)30 ,(in12)31 should never be high together
//(in11)24 ,(in21)25 should never be high together
// or the motordriver will BURN
#include <Servo.h>

Servo myservo;

String command = "";
String line_follower_start = "SLF";
String line_follower_stop = "NLF";
String stepper_id = "ST";
String goto_id = "GT";
String start_id = "GH";

int curX, dstX;
int curY, dstY;
int in11 = 25;
int in21 = 24;
int in22 = 30;
int in12 = 31;
int pwm1 = 9; //Blue
int pwm2 = 8; //Grey
int dir = 0;

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void stepperActuator(int steps) {
  String data = "Actuating stepper to " + String(steps);
  Serial.println(data);
  // actuate stepper
  myservo.write(steps);
}


void Forward(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("F :" + String(spd1) + String(spd2));
}

void Reverse(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);


  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("Reverse :" + String(spd1) + String(spd2));

}

void Right(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("R :" + String(spd1) + String(spd2));
}

void Left(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("L :" + String(spd1) + String(spd2));
}

void BiLeft(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("BIL :" + String(spd1) + String(spd2));
}

void BiRight(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("BIR :" + String(spd1) + String(spd2));
}

void Rotate_St() {
  BiRight(220, 220);
  delay(300);
  while (!(digitalRead(5) && digitalRead(6))) {
    BiRight(220, 220);
  }
}

void wait() {

  digitalWrite(in11, LOW);
  digitalWrite(in21, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
  Serial.println("waiting....");
}

void setup() {
  pinMode(in11, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(in21, OUTPUT);
  pinMode(in22, OUTPUT);

  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  Serial.begin(9600);
  Serial.flush();
  // put your setup code here, to run once:

}

void loop() {
  if (Serial.available()) {
    command = Serial.readString();
    if (command.startsWith("F")) {
      Forward(25, 25);
    } else if (command.startsWith("R")) {
      Right(20, 30);
    } else if (command.startsWith("L")) {
      Left(30, 20);
    } else if (command.startsWith("BR")) {
      BiRight(50, 50);
      delay(1500);
      wait();
      delay(1000);
    } else if (command.startsWith("BL")) {
      BiLeft(35, 35);
    } else if (command.startsWith("I")) {
      Reverse(30, 30);

    } else if (command.startsWith(stepper_id)) {
      int steps = getValue(command, '-', 1).toInt();
      stepperActuator(steps);
    } else {
      wait();
    }
  }
}

