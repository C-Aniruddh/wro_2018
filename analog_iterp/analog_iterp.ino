
bool LNFS = false;
bool modR = false;

//RIGHT MOTOR
const byte in11 = 25;
const byte in21 = 24;
const byte pwm1 = 11;
//LEFT MOTOR
const byte in22 = 30;
const byte in12 = 31;
const byte pwm2 = 10;

const byte analogPin = A0;   // Connect AN output of LSA08 to analog pin 0
const byte junctionPulse = 4;// Connect JPULSE of LSA08 to pin 4

int dir = 0;
int curX, dstX;
int curY, dstY;
int readVal, positionVal;// Variables to store analog and line position value


String command = "";
String line_follower_start = "SLF";
String line_follower_stop = "NLF";
String stepper_id = "ST";
String goto_id = "GT";
String start_id = "GH";
String push_id = "PSH";

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

void Forward(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("F :" + String(spd1) + String(spd2));
}

void Reverse(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);


  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("Reverse :" + String(spd1) + String(spd2));

}

void Right(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("R :" + String(spd1) + String(spd2));
}

void Left(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("L :" + String(spd1) + String(spd2));
}

void BiLeft(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("BIL :" + String(spd1) + String(spd2));
}

void BiRight(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("BIR :" + String(spd1) + String(spd2));
}

void Rotate_St() {
  BiRight(41, 46);
  delay(300);
  while (!(digitalRead(5) && digitalRead(6))) {
    BiRight(41, 46);
  }
}

void wait() {

  digitalWrite(in11, LOW);
  digitalWrite(in21, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, 0);
  analogWrite(pwm2, 0);
  //Serial.println("waiting....");
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
        delay(1800);
        Reverse(30, 30);
        curX++;
        dir = 2;
      }
    } else {
      modR = false;
      BiRight(41, 46);
      delay(3000);
      Forward(26, 26);
      dir = 3;
      curY--;

    }
  } else if (dir == 2) {
    BiRight(41, 46);
    delay(1800);
    Forward(26, 26);
    dir = 0;
    curX++;
  } else {
    BiRight(41, 46);
    delay(1800);
    Forward(26, 26);
    dir = 0;
    curX++;
  }

}

void curYLower() {
  if (dir == 0) {
    BiRight(41, 46);
    delay(1800);
    Forward(26, 26);
    dir = 1;
    curY++;
  } else if (dir == 1) {
    Forward(26, 26);
    dir = 1;
    curY++;
  } else if (dir == 2) {
    BiLeft(47, 47);
    delay(1800);
    Forward(26, 26);
    dir = 1;
    curY++;
  } else {
    BiRight(41, 46);
    delay(1800);
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
    BiRight(41, 46);
    delay(1800);
    Forward(26, 26);
    dir = 3;
    curY--;
  } else if (dir == 2) {
    BiLeft(47, 47);
    delay(1800);
    dir = 3;
  } else {
    BiRight(41, 46);
    delay(1800);
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
  //Serial.println(str);
  str = "Destination :" + String(dstX) + String(dstY);
  //Serial.println(str);
  //Serial.println(dir);
  if ((curX == dstX) && (curY == dstY)) {
    //Serial.println("Waiting for new destination");
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
    //Serial.println("What Case is Left");
  }

}


void junctionManager() {
  Reverse(1, 1);
  stopLineFollow();
  goto_act();
  delay(600);
  startLineFollow();
}


void LSA_Manager() {
  Serial.println(String(positionVal));


  if (digitalRead(junctionPulse)) {
    while (digitalRead(junctionPulse)) {
      junctionManager();
    }
  }

  readVal = analogRead(analogPin);    // Read value from analog pin

  // Convert voltage level into line position value
  positionVal = ((float)readVal / 921) * 70;
  // Line at left when 0 - 18, move left
  if (positionVal <= 28)
    Left(32, 18);

  // Line at middle when 19 - 52, move forward
  else if (positionVal <= 42)
    Forward(28, 29);

  // Line at right when 53 - 70, move right
  else if (positionVal <= 70)
    Right(18, 32);

  // If no line is detected, stay at the position
  else
    wait();

  // Put some delay to avoid the robot jig while making a turn
}


void stopLineFollow() {
  //Serial.println("Stop Line Follower");
  LNFS = false;
  wait();
}
void startLineFollow() {
  //Serial.println("Start Line Follower");
  LNFS = true;
}

void Push() {
  Forward(70, 70);
  delay(100);
  wait();
}

void goHome() {
  Forward(26, 26);
  delay(1800);
  BiLeft(47, 47);
  delay(1800);
}

void setup() {

  pinMode(junctionPulse, INPUT);
  pinMode(analogPin, INPUT);

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
    delay(100);
  }
}

