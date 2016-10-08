int incoming[2];
boolean value;
boolean recieved();
void make_move_red(int inc);
void make_move_blue(int inc1); 
int pins[] = {2,3,4,5,6,7,8,9}; //pins

void setup() {
   Serial.begin(9600);
   Serial.print("Starting");
   
  for(int i=0;i<8;i++) {
    pinMode(pins[i],OUTPUT);
  }
}

void loop() {
  recieved();
  if(recieved()) {
  make_move_red(incoming[0]); 
  make_move_blue(incoming[1]);
  }
  else { 
      printf("not enough bytes recieved"); 
  }
}

boolean recieved() {
   
   if(Serial.available() >= 2){
    for(int j = 0;j<2;j++) {
      incoming[j] = Serial.read();
    }
    value = true;
   }
   else { 
   value = false;
   }
   return value;
}

void make_move_red(int inc) { 
  if(inc == 1) {        //49
     digitalWrite(2,HIGH);
     digitalWrite(3,LOW);
     digitalWrite(4,LOW);
     digitalWrite(5,LOW);
  }
  else if(inc == 2) {   //50
     digitalWrite(2,LOW);
     digitalWrite(3,HIGH);
     digitalWrite(4,LOW);
     digitalWrite(5,LOW);
  }
  else if(inc == 4) {   //52
     digitalWrite(2,LOW);
     digitalWrite(3,LOW);
     digitalWrite(4,HIGH);
     digitalWrite(5,LOW);
  }
  else if(inc == 8) {  //56
     digitalWrite(2,LOW);
     digitalWrite(3,LOW);
     digitalWrite(4,LOW);
     digitalWrite(5,HIGH);
  }
  else if(inc == 5) {   //53
     digitalWrite(2,HIGH);
     digitalWrite(3,LOW);
     digitalWrite(4,HIGH);
     digitalWrite(5,LOW);
  }
  else if(inc == 9) {    //57
     digitalWrite(2,HIGH);
     digitalWrite(3,LOW);
     digitalWrite(4,LOW);
     digitalWrite(5,HIGH);
  }
  else if(inc == 6) {    //54
     digitalWrite(2,LOW);
     digitalWrite(3,HIGH);
     digitalWrite(4,HIGH);
     digitalWrite(5,LOW);
  }
  else if(inc == 10) {
     digitalWrite(2,LOW);
     digitalWrite(3,HIGH);
     digitalWrite(4,LOW);
     digitalWrite(5,HIGH);
  }
  else { 
     digitalWrite(2,LOW);
     digitalWrite(3,LOW);
     digitalWrite(4,LOW);
     digitalWrite(5,LOW); 
  }
}

void make_move_blue(int inc1) { 
  printf("in blue");
  if(inc1 == 1) {        //49
     digitalWrite(6,HIGH);
     digitalWrite(7,LOW);
     digitalWrite(8,LOW);
     digitalWrite(9,LOW);
  }
  else if(inc1 == 2) {   //50
     digitalWrite(6,LOW);
     digitalWrite(7,HIGH);
     digitalWrite(8,LOW);
     digitalWrite(9,LOW);
  }
  else if(inc1 == 4) {   //52
     digitalWrite(6,LOW);
     digitalWrite(7,LOW);
     digitalWrite(8,HIGH);
     digitalWrite(9,LOW);
  }
  else if(inc1 == 8) {  //56
     digitalWrite(6,LOW);
     digitalWrite(7,LOW);
     digitalWrite(8,LOW);
     digitalWrite(9,HIGH);
  }
  else if(inc1 == 5) {   //53
     digitalWrite(6,HIGH);
     digitalWrite(7,LOW);
     digitalWrite(8,HIGH);
     digitalWrite(9,LOW);
  }
  else if(inc1 == 9) {    //57
     digitalWrite(6,HIGH);
     digitalWrite(7,LOW);
     digitalWrite(8,LOW);
     digitalWrite(9,HIGH);
  }
  else if(inc1 == 6) {    //54
     digitalWrite(6,LOW);
     digitalWrite(7,HIGH);
     digitalWrite(8,HIGH);
     digitalWrite(9,LOW);
  }
  else if(inc1 == 10) {
     digitalWrite(6,LOW);
     digitalWrite(7,HIGH);
     digitalWrite(8,LOW);
     digitalWrite(9,HIGH);
  }
  else { 
     digitalWrite(6,LOW);
     digitalWrite(7,LOW);
     digitalWrite(8,LOW);
     digitalWrite(9,LOW); 
  }
}



