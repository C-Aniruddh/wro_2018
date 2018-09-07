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
String push_id = "PSH";

int curX, dstX;
int curY, dstY;
int in11 = 25;
int in21 = 24;
int in22 = 30;
int in12 = 31;
int pwm1 = 11; //Blue
int pwm2 = 10; //Grey
int dir = 0;

bool LNFS = false;
bool modR = false;

String getValue(String data, char separator, int index) {
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

void stopLineFollow() {
  Serial.println("Stop Line Follower");
  LNFS = false;
  wait();
}
void startLineFollow() {
  Serial.println("Start Line Follower");
  LNFS = true;
}

void setMotorDir() {
  if (modR == false) {
    digitalWrite(in11, LOW);
    digitalWrite(in22, LOW);
    digitalWrite(in12, HIGH);
    digitalWrite(in21, HIGH);
  } else {
    digitalWrite(in11, HIGH);
    digitalWrite(in22, HIGH);
    digitalWrite(in12, LOW);
    digitalWrite(in21, LOW);
  }
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
  BiRight(43, 43);
  delay(300);
  while (!(digitalRead(5) && digitalRead(6))) {
    BiRight(43, 43);
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
    Forward(26, 26);
    dir = 0;
    curX++;
  } else if (dir == 1) {
    if (dstX == 2 && dstY == 0) {
      modR = true;
      if (curX == 1 && curY == 1) {
        Reverse(30, 30);
        curY--;
      } else if (curX == 1 && curY == 0) {
        BiLeft(47, 47);
        delay(1600);
        Reverse(30, 30);
        curX++;
        dir = 2;
      }
    } else {
      modR = false;
      BiRight(43, 43);
      delay(3000);
      Forward(26, 26);
      dir = 3;
      curY--;

    }
  } else if (dir == 2) {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
    dir = 0;
    curX++;
  } else {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
    dir = 0;
    curX++;
  }

}

void curYLower() {
  if (dir == 0) {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
    dir = 1;
    curY++;
  } else if (dir == 1) {
    Forward(26, 26);
    dir = 1;
    curY++;
  } else if (dir == 2) {
    BiLeft(47, 47);
    delay(1600);
    Forward(26, 26);
    dir = 1;
    curY++;
  } else {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
    dir = 1;
    curY++;
  }
}

void curYHigher() {
  if (dir == 0) {
    Forward(26, 26);
    dir = 0;
    curY--;
  } else if (dir == 1) {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
    dir = 3;
    curY--;
  } else if (dir == 2) {
    BiLeft(47, 47);
    delay(1600);
    dir = 3;
  } else {
    BiRight(43, 43);
    delay(1600);
    Forward(26, 26);
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
  stopLineFollow();
  goto_act();
  delay(600);
  startLineFollow();
}

void LSA_Manager() {
  //Check Junction
  for (int i = 2; i <= 9; i++) {
    Serial.print(digitalRead(i));
  }
  Serial.println();
  //bool junction = true;
  //Check Junction
  bool junction =  digitalRead(5) && digitalRead(2) && digitalRead(6) && digitalRead(9);
  if (junction) {
    wait();
    delay(500);
    junctionManager();
    delay(100);
  } else if ((digitalRead(3) && digitalRead(2)) ||
             (digitalRead(4) && digitalRead(3)) ||
             (digitalRead(5) && digitalRead(3)) ||
             (digitalRead(2) || digitalRead(3))) {
    //Right(23, 31);
    Left(31, 23);
    //delay(100);

  } else if ((digitalRead(8) && digitalRead(7)) ||
             (digitalRead(9) && digitalRead(8)) ||
             (digitalRead(7) && digitalRead(9)) ||
             (digitalRead(9) || digitalRead(8))) {

    //Left(31, 23);
    Right(23, 31);
    //delay(100);

  } else if ((digitalRead(2) && digitalRead(3) &&
               digitalRead(4) && digitalRead(5) &&
               digitalRead(6) && digitalRead(7) &&
               digitalRead(8) && digitalRead(9)) == 0) {
    wait();

  } else {
    if (modR == true) {
      Reverse(28, 28);
    } else {
      Forward(28, 28);
    }
  }
  //  LNFS = true;
}

void Push() {
  Forward(70, 70);
  delay(100);
}

void goHome() {
  Forward(28, 28);
  delay(1600);
  BiLeft(47, 47);
  delay(1600);
}

void setup() {
  // put your setup code here, to run once:
  // myservo.attach(10);
  pinMode(in11, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(pwm1, OUTPUT);

  pinMode(in21, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(pwm2, OUTPUT);

  Serial.begin(9600);
  Serial.flush();

  curX = 0;
  curY = 0;
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
    } else if (command.startsWith(push_id)) {
      Push();
    } else {}
  }
  if (LNFS == true) {
    LSA_Manager();
    delay(50);
  }
}

