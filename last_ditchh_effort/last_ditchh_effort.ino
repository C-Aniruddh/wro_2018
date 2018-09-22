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
String gtStack_id = "ST";
String goto_id = "GT";
String start_id = "GH";
String push_id = "PSH";
String sr_id = "SR";

const byte LSA_val = A13;   // Connect AN output of LSA08 to analog pin 0
const byte junctionPulse = 10;   // Connect JPULSE of LSA08 to pin 4
const byte trigFront = 3 ;
const byte echoFront = 2;
const byte trigBack = 5 ;
const byte echoBack = 4;
const byte VCC_back = A0;


int i = 0;
int curX, dstX;
int curY, dstY;
int in11 = 25;
int in21 = 24;
int in22 = 30;
int in12 = 31;
int pwm1 = 9; //Blue
int pwm2 = 8; //Grey
int dir = 0; //set dir as 0
int blockNum = 2;
int back_distance = 17; //in cm
int front_distance = 22; //in cm

long duration, distance;

float baseSpeed = 23;
float  maxSpeed = 32;
float offset = -5;
float Kp = 0.5;
float Ki = 0;
float Kd = 0.5;
float setPoint = 35;
float lastError = 0;
float elapsedTime, timeNow, timePrev;

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
  //Serial.println("Stop Line Follower");
  LNFS = false;
  wait();
}
void startLineFollow() {
  //Serial.println("Start Line Follower");
  LNFS = true;
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
  //////Serial.println("Reverse :" + String(spd1) + String(spd2));

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

void BiLeft(int spd1, int spd2) {
  digitalWrite(in11, LOW);
  digitalWrite(in21, HIGH);
  digitalWrite(in12, LOW);
  digitalWrite(in22, HIGH);

  analogWrite(pwm1, spd1);
  analogWrite(pwm2, spd2);
  //Serial.println("BIL :" + String(spd1) + String(spd2));
}

void Rotate() {
  startLineFollow();
  BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
  while (float((analogRead(LSA_val)) * (70 / 921)) > 32 &&
         (float(analogRead(LSA_val)) * (70 / 921) < 38)) {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
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
void stepperActuator(int steps) {
  String data = "Actuating stepper to " + String(steps);
  //Serial.println(data);
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
    Forward(27, 27);
    dir = 0;
    curX++;
  } else if (dir == 1) {
    if (dstX == 2 && dstY == 0) {
      modR = true;
      if (curX == 1 && curY == 1) {
        Reverse(30, 30);
        curY--;
      } else if (curX == 1 && curY == 0) {
        BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
        delay(1850);
        Reverse(30, 30);
        curX++;
        Forward(30, 30);
        delay(400);
        dir = 2;
      }
    } else {
      modR = false;
      BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
      delay(3000);
      Forward(28, 28);
      dir = 3;
      curY--;

    }
  } else if (dir == 2) {
    if (modR == true) {
      Reverse(28, 28);
    } else {
      BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
      delay(1850);
    }

    dir = 0;
    curX++;
  } else {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 0;
    curX++;
  }

}

void curYLower() {
  if (dir == 0) {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 1;
    curY++;
  } else if (dir == 1) {
    Forward(27, 27);
    dir = 1;
    curY++;
  } else if (dir == 2) {
    if (modR == true) {
      Reverse(28, 28);
    }
    BiLeft(42 + (2 * blockNum), 40 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 1;
    curY++;
  } else {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 1;
    curY++;
  }
}

void curYHigher() {
  if (dir == 0) {
    Forward(27, 27);
    dir = 0;
    curY--;
  } else if (dir == 1) {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 3;
    curY--;
  } else if (dir == 2) {
    BiLeft(42 + (2 * blockNum), 40 + (2 * blockNum));
    delay(1850);
    dir = 3;
  } else {
    BiRight(44 + (2 * blockNum), 42 + (2 * blockNum));
    delay(1850);
    Forward(28, 28);
    dir = 1;
    curY--;
  }
}

void curXHigher() {
  //Serial.println("This shouldnt happpen for us");
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
  delay(800);
  startLineFollow();
  if (curX == 1, curY == 0) {
    Serial.println("R");
  }
}

void LP() {
  Forward(35, 35);
  delay(1500);
}


void LSA_Manager() {

  //Serial.println("Pulse : " + String(digitalRead(junctionPulse)));

  int readVal = analogRead(LSA_val);
  int positionVal  = ((float)readVal / 921) * 70;
  //Serial.println("LSA Value :" + String(positionVal));
  // If no line is detected, stay at the position
  bool junct = digitalRead(junctionPulse);
  if (curX == 2 && curY == 0 ) {
    junct = false;
  }
  if (junct) {
    wait();
    delay(500);
    junctionManager();
    delay(100);
  } else {
    float error = positionVal - setPoint  + offset;   // Calculate the deviation from position to the set point
    float motorSpeed = (Kp * error) + (Kd * (error - lastError) / elapsedTime); // Applying formula of PID
    lastError = error;    // Store current error as previous error for next iteration use

    // Adjust the motor speed based on calculated value
    // You might need to interchange the + and - sign if your robot move in opposite direction
    float rightMotorSpeed = baseSpeed - motorSpeed;
    float leftMotorSpeed = baseSpeed + motorSpeed;

    // If the speed of motor exceed max speed, set the speed to max speed
    if (rightMotorSpeed > maxSpeed) {
      rightMotorSpeed = maxSpeed;
    }
    if (leftMotorSpeed > maxSpeed) {
      leftMotorSpeed = maxSpeed;
    }

    // If the speed of motor is negative, set it to 0
    if (rightMotorSpeed < 0) {
      rightMotorSpeed = 0;
    }
    if (leftMotorSpeed < 0) {
      leftMotorSpeed = 0;
    }

    // Writing the motor speed value as output to hardware motor
    if (modR == false) {
      Forward((int(rightMotorSpeed)), int(leftMotorSpeed + 11));
    } else {
      Reverse((int(rightMotorSpeed)), int(leftMotorSpeed + 11));
    }

  }
  // Else if line detected, calculate the motor speed and apply
  //Check Junction
  //  LNFS = true;
}

void frontUS() {
  digitalWrite(trigFront, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigFront, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigFront, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoFront, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2;

  // Prints the distance on the Serial Monitor
  //Serial.println("Distance Front : " + String(distance));

  if (distance <= front_distance) {
    Reverse(1, 1);
    stopLineFollow();
  }
}


void BackUS() {
  digitalWrite(trigBack, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigBack, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigBack, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoBack, HIGH);

  // Calculating the distance
  long distance = duration * 0.034 / 2;

  // Prints the distance on the Serial Monitor
  //Serial.println("Distance Back: " + String(distance));

  if (distance <= back_distance) {
    Reverse(1, 1);
    Serial.println("E");
    delay(200);
    stopLineFollow();

  }
}


void SlightReverse() {
  Reverse(60, 60);
  delay(100);
  wait();
  i++;
  if (i == 2) {
    Forward(50, 50);
    delay(1000);
    wait();
  }

}

void Push() {
  Forward(70, 70);
  delay(150);
  wait();
}

void goHome() {
  Reverse(30, 55);
  delay(1650);
  BiLeft(44, 42);
  delay(2000);
  //Forward(70,70);
  // delay(200);
  modR = true;
  dir = 2;
  wait();
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

  pinMode(junctionPulse, INPUT);
  pinMode(LSA_val, INPUT);

  pinMode(trigBack, OUTPUT);
  pinMode(echoBack, INPUT);
  pinMode(trigFront, OUTPUT);
  pinMode(echoFront, INPUT);
  pinMode(VCC_back, OUTPUT);


  Serial.begin(9600);
  Serial.flush();
  //Serial.println(Serial.available());
  //set (0,0)
  curX = 0;
  curY = 0;
}


void loop() {

  analogWrite(A0, 255);
  timePrev = timeNow;
  timeNow  = millis();
  elapsedTime = (timeNow - timePrev) / 1000;
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    command = Serial.readString();
    if (command.startsWith(line_follower_start)) {
      startLineFollow();
    } else if (command.startsWith(line_follower_stop)) {
      stopLineFollow();
    } else if (command.startsWith(gtStack_id)) {
      if (dstX == 2 && dstY == 0) {
        junctionManager();
      }
    } else if (command.startsWith(goto_id)) {
      dstX = getValue(command, '-', 1).toInt();
      dstY = getValue(command, '-', 2).toInt();
      //Serial.println("Going to :" + String(dstX) + String(dstY));
    } else if (command.startsWith(start_id)) {
      goHome();
      Serial.println("Going Home");
    } else if (command.startsWith(push_id)) {
      Push();
    } else if (command.startsWith(sr_id)) {
      SlightReverse();
    } else if (command.startsWith("LP")) {
      LP();
    }

    else {}
  }
  if (LNFS == true) {
    LSA_Manager();
    if (dstX == 1 and dstY == 1) {
      frontUS();
    }
    delay(100);
  }
  if (modR) {
    BackUS();
  }
}

