#include <Servo.h>

Servo myservo;

String command = "";
String line_follower_start = "LNFS";
String line_follower_stop = "LNFST";
String stepper_id = "ST";
String goto_id = "GT";

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myservo.attach(9);
}

void startLineFollow(){
  Serial.println("Starting line follower");  
}

void stopLineFollow(){
  Serial.println("Stopping line follower");
}

void stepperActuator(int steps){
  String data = "Actuating stepper to " + String(steps);
  Serial.println(data);
  // actuate stepper  
  myservo.write(steps);
}

void goto_act(int x, int y){
  String data = "Going to " + String(x) + ", " + String(y);
  Serial.println(data);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    command = Serial.readString();
    if (command.equals(line_follower_start)){
      startLineFollow();  
    } else if (command.equals(line_follower_stop)){
      stopLineFollow();  
    } else if (command.startsWith(stepper_id)){
      int steps = getValue(command, '-', 1).toInt();
      stepperActuator(steps);
    } else if (command.startsWith(goto_id)){
      int x = getValue(command, '-', 1).toInt();
      int y = getValue(command, '-', 2).toInt();
      goto_act(x, y);
    }
  }
}
