/*
  ReadAnalogVoltage

  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
/////for k=1:n-1, for i=k+1:n , for k=k:n+1, a(i,j)= a(i,j) - a(k,j)*a(i,k)/a(k,k);end;for j=i:k,a(i,j)=0;end;end;end;
  http://www.arduino.cc/en/Tutorial/ReadAnalogVoltage
*/
int rpm=100,nofjunctions=0;
uint16_t left_val,center_val,right_val,fleft=0,fcenter=0,fright=0;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(57600);
  pinMode(22,OUTPUT); //A0
  pinMode(23,OUTPUT); //A1
  pinMode(24,OUTPUT); //A2
  pinMode(25,OUTPUT); //A3
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(17,OUTPUT);
}

void forward(int data)
{
  PORTA = 0B00001010;
  analogWrite(6,data);
  analogWrite(7,data);
}
void backward(int data)
{
  PORTA = 0B00000101;
  analogWrite(6,data);
  analogWrite(7,data);
}
void left (int data)
{
  PORTA = 0B00001001;
  analogWrite(6,data);
  analogWrite(7,data);
}
void right (int data)
{
  PORTA = 0B00000110;
  analogWrite(6,data);
  analogWrite(7,data);
}
void soft_right (int data)
{
  PORTA = 0B00000010;
  analogWrite(6,data);
  analogWrite(7,data);
}
void soft_left (int data)
{
  PORTA = 0B00001000;
  analogWrite(6,data);
  analogWrite(7,data);
}
void stop_motor(int data=0)
{
  PORTA &= 0B00000000;
  analogWrite(6,data);
  analogWrite(7,data);
}
int is_black(uint16_t data)
{
  if (data > 125)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}
void follow()
{
  while(1)
  {
  left_val = analogRead(A0);
  center_val = analogRead(A1);
  right_val = analogRead(A2);
  if (( !is_black(right_val) && !is_black(center_val) && !is_black(left_val) ))
  {
    left_val=fleft;
    right_val=fright;
    center_val=fcenter;
  }
  if (is_black(center_val) && !is_black(right_val) && !is_black(left_val))
  {
    forward(rpm);
  }
  if (is_black(right_val)) //|| (is_black(right_val) && is_black(center_val) && !is_black(left_val)))
  {
    soft_right(rpm);
  }
  if (is_black(left_val)) // || (!is_black(right_val) && is_black(center_val) && is_black(left_val)))
  {
    soft_left(rpm);
  }
  if (junction_detection(left_val,right_val,center_val))
  {
    if (1)
    {
       right_junction();
    } 
    break;
  }
  fleft=left_val;
  fright=right_val;
  fcenter=center_val;
  }
  return ;
}

void right_junction()
{
      forward(rpm);
      delay(150);
      left_val = analogRead(A0);
      center_val = analogRead(A1);
      right_val = analogRead(A2);
      stop_motor(0);
      while(!is_black(right_val) || !is_black(center_val))
      {
        left_val = analogRead(A0);
        center_val = analogRead(A1);
        right_val = analogRead(A2);
        soft_right(rpm);
      }
      if (is_black(center_val))
      {
        return;
      }
      while(!is_black(center_val))
      {
        left_val = analogRead(A0);
        center_val = analogRead(A1);
        right_val = analogRead(A2);
        soft_right(rpm-10);
      }
}

int junction_detection(int left_val,int right_val,int center_val)
{
 if ((is_black(left_val) && is_black(center_val) && is_black(right_val)))
 {
  return 1; 
 }
 else return 0;
}
// the loop routine runs over and over again forever:



void follow_line()
{
  while(1)
  {
  left_val = analogRead(A0);
  center_val = analogRead(A1);
  right_val = analogRead(A2);
  digitalWrite(17,LOW);
  if (!is_black(left_val) && !is_black(center_val) && !is_black(right_val))
  {
    left_val=fleft;
    center_val=fcenter;
    right_val=fright;
  }
  if (!is_black(left_val) && !is_black(center_val) && is_black(right_val))
  {
    soft_right(rpm);
    continue;
  }
  if (!is_black(left_val) && is_black(center_val) && !is_black(right_val))
  {
    forward(rpm);
    continue;
  }
  if (!is_black(left_val) && is_black(center_val) && is_black(right_val))
  {
    /*while(!(!is_black(left_val) && !is_black(center_val) && is_black(right_val)))
    {
      soft_right(rpm);
    }
    continue;*/
  }
  if (is_black(left_val) && !is_black(center_val) && !is_black(right_val))
  {
    soft_left(rpm);
    continue;
  }
  if (is_black(left_val) && !is_black(center_val) && is_black(right_val))
  {
    ;//////// shyit //////
  }
  if (is_black(left_val) && is_black(center_val) && !is_black(right_val))
  {
    /*while(!(is_black(left_val) && !is_black(center_val) && !is_black(right_val)))
    {
      soft_left(rpm);
    }
    continue;*/
  }
  if (is_black(left_val) && is_black(center_val) && is_black(right_val))
  {
    ////node
    stop_motor();
    delay(500);
    digitalWrite(17,HIGH);
    delay(250);
    digitalWrite(17,LOW);
    forward(rpm);
    delay(200);
    stop_motor(0);
    delay(100);
    if (1) // after node go left
    {
      left_val = analogRead(A0);
      center_val = analogRead(A1);
      right_val = analogRead(A2);
      forward(rpm);
      delay(200);
      stop_motor(rpm);
      delay(100);
      left(rpm);
      delay(125);
      stop_motor();
      while( !is_black(left_val) )
      {
        left_val = analogRead(A0);
        soft_left(rpm);
      }
    }
    if (0) // after node go right
    {
      left_val = analogRead(A0);
      center_val = analogRead(A1);
      right_val = analogRead(A2);
      forward(rpm);
      delay(50);
      right(rpm);
      delay(125);
      stop_motor();
      while( !is_black(right_val) )
      {
        right_val = analogRead(A0);
        soft_left(rpm);
      }
   }
  }  
  
  fleft=left_val;
  fright=right_val;
  fcenter=center_val;
  }
}
void loop() {
  follow_line();
}
