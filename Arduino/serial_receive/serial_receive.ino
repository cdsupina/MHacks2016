int value[2];
void make_move_blue();
int del = 50;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
}

void loop() {
   if(Serial.available() >= 2) {
    for(int i=0;i<2;i++) {
        value[i] = Serial.read();
    }
    make_move_red();
    make_move_blue();
   }
}

void make_move_red() {
  if(value[0] == 1) {
    digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
    digitalWrite(5,LOW);
    delay(del);
    digitalWrite(2,LOW);
  }
  else if(value[0] == 2) {
    digitalWrite(2,LOW);
    digitalWrite(3,HIGH);
    digitalWrite(4,LOW);
    digitalWrite(5,LOW);
    delay(del);
    digitalWrite(3,LOW);
  }
  else if(value[0] == 4) {
    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,HIGH);
    digitalWrite(5,LOW);
    delay(del);
    digitalWrite(4,LOW);
  }
  else if(value[0] == 8) {
    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
    digitalWrite(5,HIGH);
    delay(del);
    digitalWrite(5,LOW);
  }
  else if(value[0] == 5) {
    digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
    digitalWrite(4,HIGH);
    digitalWrite(5,LOW);
    delay(del);
    digitalWrite(2,LOW);
    digitalWrite(4,LOW);
  }
  else if(value[1] == 9) {
    digitalWrite(2,HIGH);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
    digitalWrite(5,HIGH);
    delay(del);
    digitalWrite(2,LOW);
    digitalWrite(5,LOW);
  }
  else if(value[1] == 6) {
    digitalWrite(2,LOW);
    digitalWrite(3,HIGH);
    digitalWrite(4,HIGH);
    digitalWrite(5,LOW);
    delay(del);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
  }
  else if(value[1] == 10) {
    digitalWrite(2,LOW);
    digitalWrite(3,HIGH);
    digitalWrite(4,LOW);
    digitalWrite(5,HIGH);
    delay(del);
    digitalWrite(3,LOW);
    digitalWrite(5,LOW);
  }
  else {
    digitalWrite(2,LOW);
    digitalWrite(3,LOW);
    digitalWrite(4,LOW);
    digitalWrite(5,LOW);
  }
}

void make_move_blue() {
  if(value[1] == 1) {
    digitalWrite(6,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
    delay(del);
    digitalWrite(6,LOW);
  }
  else if(value[1] == 2) {
    digitalWrite(6,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
    delay(del);
    digitalWrite(7,LOW);
  }
  else if(value[1] == 4) {
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,HIGH);
    digitalWrite(9,LOW);
    delay(del);
    digitalWrite(8,LOW);
  }
  else if(value[1] == 8) {
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,HIGH);
    delay(del);
    digitalWrite(9,LOW);
  }
  else if(value[1] == 5) {
    digitalWrite(6,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(8,HIGH);
    digitalWrite(9,LOW);
    delay(del);
    digitalWrite(6,LOW);
    digitalWrite(8,LOW);
  }
  else if(value[1] == 9) {
    digitalWrite(6,HIGH);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,HIGH);
    delay(del);
    digitalWrite(6,LOW);
    digitalWrite(9,LOW);
  }
  else if(value[1] == 6) {
    digitalWrite(6,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(8,HIGH);
    digitalWrite(9,LOW);
    delay(del);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
  }
  else if(value[1] == 10) {
    digitalWrite(6,LOW);
    digitalWrite(7,HIGH);
    digitalWrite(8,LOW);
    digitalWrite(9,HIGH);
    delay(del);
    digitalWrite(7,LOW);
    digitalWrite(9,LOW);
  }
  else {
    digitalWrite(6,LOW);
    digitalWrite(7,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
  }
}
