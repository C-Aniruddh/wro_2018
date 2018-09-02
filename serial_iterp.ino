//github.com/C-Aniruddh/wro_2018/tree/wro_doshi

//(in22)30 ,(in12)31 should never be high together
//(in11)24 ,(in21)25 should never be high together
// or the motordriver will BURN

//12345678
//23456789

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
int in11 = 24;
int in21 = 25;
int in22 = 30;
int in12 = 31;
int pwm1 = 11;
int pwm2 = 12;
int dir = 0;

bool LNFS = false;
bool modR = false;

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

void Forward(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in22, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in21, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("F :" + String(spd1) + String(spd2));
}

void Reverse(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in22, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in21, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("Reverse :" + String(spd1) + String(spd2));

}

void Right(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in22, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in21, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("R :" + String(spd1) + String(spd2));
}

void Left(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in22, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in21, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("L :" + String(spd1) + String(spd2));
}

void BiLeft(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in22, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in21, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("BIL :" + String(spd1) + String(spd2));
}

void BiRight(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in22, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in21, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial.println("BIR :" + String(spd1) + String(spd2));
}

void wait() {

  digitalWrite(in11, LOW);
  digitalWrite(in22, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in21, LOW);

  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
  Serial.println("waiting....");

}

void Rotate_St() {
  while (digitalRead(5) && digitalRead(6)) {
    BiRight(220, 220);
  }
}

void stepperActuator(int steps) {
  String data = "Actuating stepper to " + String(steps);
  Serial.println(data);
  // actuate stepper
  myservo.write(steps);
}

void XEqual() {
  if (curY < dstY) {
    curYLower();
  } else {
    curYHigher();
  }
}

void YEqual() {
  if (curX < dstX) {
    curXLower();
  } else {
    curXHigher();
  }
}

void curXLower() {
  if (dir == 0) {
    Forward(170, 170);
    dir = 0;
    curX++;
  } else if (dir == 1) {
    BiRight(220, 220);
    delay(3000);
    Forward(170, 170);
    dir = 3;
    curY--;
  } else if (dir == 2) {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 0;
    curX++;
  } else {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 0;
    curX++;
  }

}

void curYLower() {
  if (dir == 0) {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 1;
    curY++;
  } else if (dir == 1) {
    Forward(170, 170);
    dir = 1;
    curY++;
  } else if (dir == 2) {
    BiLeft(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 1;
    curY++;
  } else {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 1;
    curY++;
  }
}

void curYHigher() {
  if (dir == 0) {
    Forward(170, 170);
    dir = 0;
    curY--;
  } else if (dir == 1) {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 3;
    curY--;
  } else if (dir == 2) {
    BiLeft(190, 190);
    delay(1700);
    dir = 3;
  } else {
    BiRight(220, 220);
    delay(1700);
    Forward(170, 170);
    dir = 1;
    curY--;
  }
}

void curXHigher() {
  Serial.println("This shouldnt happpen for us");
}

void goto_act() {
  String str = "Current :" + String(curX) + String(curY);
  Serial.println(str);
  str = "Destination :" + String(dstX) + String(dstY);
  Serial.println(str);
  Serial.println(dir);
  if ((curX == dstX) && (curY == dstY)) {
    Serial.println("Waiting for new destination");
  } else if (curX == dstX) {
    XEqual();
  } else if (curY == dstY) {
    YEqual();
  } else if (curX < dstX) {
    curXLower();
  } else if (curY < dstY) {
    curYLower();
  } else if (curY > dstY) {
    curYHigher();
  } else if (curX > dstX) {
    curXHigher();
  } else {
    Serial.println("What Case is Left");
  }

}


void junctionManager() {
  goto_act();
}

void LSA_Manager() {
  //Check Junction
  for (int i = 2; i <= 9; i++) {
    Serial.print(digitalRead(i));
  }
  //01234567
  //23456789
  Serial.println();
  //bool junction = true;
  //Check Junction
  bool junction = digitalRead(2) && digitalRead(6) && digitalRead(9);
  if (junction) {
    wait();
    delay(500);
    junctionManager();
    delay(1000);
  } else if ((digitalRead(5) && digitalRead(4)) || (digitalRead(6) && digitalRead(4))) {
    if (modR == true) {
      Reverse(140, 140);
    } else {
      Forward(140, 140);
    }


  } else if ((digitalRead(3) && digitalRead(4)) || (digitalRead(3) || (digitalRead(2)))) {
    if (modR == true) {
      Right(190, 90);
    } else {
      Left(190, 90);
    }
    delay(200);

  } else if ((digitalRead(7) && digitalRead(6) ||
              (digitalRead(7) && digitalRead(8)) ||
              (digitalRead(8)) || (digitalRead(9)))) {
    if (modR == true) {
      Left(190, 90);
    } else {
      Right(90, 190);
    }
    delay(200);

  } else {
    wait();
  }
  //  LNFS = true;
}

void stopLineFollow() {
  Serial.println("Stop Line Follower");
  LNFS = false;
  if (curX == 2 && curY == 0) {
    Rotate_St();
  }
  wait();
}
void startLineFollow() {
  Serial.println("Start Line Follower");
  LNFS = true;
}

void goHome() {
  while (!(digitalRead(2) && digitalRead(6) && digitalRead(9))) {
    Forward(140, 140);
  }
  BiLeft(220, 220);
  delay(1700);
}

void setup() {
  // put your setup code here, to run once:
  myservo.attach(10);
  pinMode(in22, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(in11, OUTPUT);
  pinMode(in21, OUTPUT);

  for (int i = 2; i <= 9; i++) {
    pinMode(i, INPUT);
  }
  pinMode(pwm1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  Serial.begin(9600);
  Serial.flush();

  curX = 0;
  curY = 0;
  String SLF = "Start Line Follower : " + line_follower_start;
  String NLF = "Stop Line Follower : " + line_follower_stop;
  String GOTO = "GOTO Point : " + goto_id;
  String GOHome = "GOTO Home : " + start_id;
  Serial.println(SLF);
  Serial.println(NLF);
  Serial.println(GOTO);
  Serial.println(GOHome);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    command = Serial.readString();
    if (command.startsWith(line_follower_start)) {
      startLineFollow();
    } else if (command.startsWith(line_follower_stop)) {
      stopLineFollow();
    } else if (command.startsWith(stepper_id)) {
      int steps = getValue(command, '-', 1).toInt();
      stepperActuator(steps);
    } else if (command.startsWith(goto_id)) {
      dstX = getValue(command, '-', 1).toInt();
      dstY = getValue(command, '-', 2).toInt();
    } else if (command.startsWith(start_id)) {
      goHome();
    } else {}
  }
  if (LNFS == true) {
    LSA_Manager();
    delay(100);
  }
}
