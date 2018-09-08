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

int rx = 15;
int tx = 14;
int serialEn = 2;
int junctionPulse = 4;
int baseSpeed = 25;
int maxSpeed = 30;
int offset = 100;
int curX, dstX;
int curY, dstY;
int in11 = 25;
int in21 = 24;
int in22 = 30;
int in12 = 31;
int pwm1 = 11; //Blue
int pwm2 = 10; //Grey
int dir = 0;
int lastError = 0;

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

void Move(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial3.println("F :" + String(spd1) + String(spd2));
}

void Reverse(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);


  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial3.println("Reverse :" + String(spd1) + String(spd2));

}

void BiRight(int spd1, int spd2) {
  digitalWrite(in11, HIGH);
  digitalWrite(in21, LOW);
  digitalWrite(in12, HIGH);
  digitalWrite(in22, LOW);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial3.println("BIR :" + String(spd1) + String(spd2));
}

void BiLeft(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  Serial3.println("BIL :" + String(spd1) + String(spd2));
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
  Serial3.println("waiting....");
}
void stepperActuator(int steps) {
  String data = "Actuating stepper to " + String(steps);
  Serial3.println(data);
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
  Serial3.println("This shouldnt happpen for us");
}

void goto_act() {
  String str = "Current :" + String(curX) + String(curY);
  Serial3.println(str);
  str = "Destination :" + String(dstX) + String(dstY);
  Serial3.println(str);
  Serial3.println(dir);
  if ((curX == dstX) && (curY == dstY)) {
    Serial3.println("Waiting for new destination");
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
    Serial3.println("What Case is Left");
  }

}


void junctionManager() {
  Reverse(1, 1);
  stopLineFollow();
  goto_act();
  delay(800);
  startLineFollow();
}


void LSA_Manager() {
  digitalWrite(serialEn, LOW);  // Set serialEN to LOW to request UART data
  while (Serial3.available() <= 0);  // Wait for data to be available
  int positionVal = Serial3.read();    // Read incoming data and store in variable positionVal
  digitalWrite(serialEn, HIGH);   // Stop requesting for UART data

  // If no line is detected, stay at the position
  if (positionVal == 255) {
    analogWrite(pwm1, 0);
    analogWrite(pwm2, 0);
  } else if (junctionPulse) {
    wait();
    delay(500);
    junctionManager();
    delay(100);

  } else {
    int error = positionVal - setPoint + offset;   // Calculate the deviation from position to the set point
    int motorSpeed = Kp * error + Kd * (error - lastError);   // Applying formula of PID
    lastError = error;    // Store current error as previous error for next iteration use

    // Adjust the motor speed based on calculated value
    // You might need to interchange the + and - sign if your robot move in opposite direction
    int rightMotorSpeed = baseSpeed - motorSpeed;
    int leftMotorSpeed = baseSpeed + motorSpeed;

    // If the speed of motor exceed max speed, set the speed to max speed
    if (rightMotorSpeed > maxSpeed) rightMotorSpeed = maxSpeed;
    if (leftMotorSpeed > maxSpeed) leftMotorSpeed = maxSpeed;

    // If the speed of motor is negative, set it to 0
    if (rightMotorSpeed < 0) rightMotorSpeed = 0;
    if (leftMotorSpeed < 0) leftMotorSpeed = 0;

    // Writing the motor speed value as output to hardware motor
    Move(rightMotorSpeed, leftMotorSpeed);
  }

  // Else if line detected, calculate the motor speed and apply

  //Check Junction
  //  LNFS = true;
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
  // put your setup code here, to run once:
  // myservo.attach(10);
  pinMode(in11, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(pwm1, OUTPUT);

  pinMode(in21, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(pwm2, OUTPUT);

  pinMode(serialEn, OUTPUT);
  pinMode(junctionPulse, INPUT);


  Serial.begin(9600);
  Serial.flush();

  Serial3.begin(9600);
  Serial3.flush();

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
    delay(100);
  }
}

