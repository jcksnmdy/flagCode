//Code created by Ian Buckley for an article on makeuseof.com


//define pins for the red, green and blue LEDs
#define RED_LEDsmall 2
#define GREEN_LEDsmall 3
#define BLUE_LEDsmall 4


#define RED_LEDmed 5
#define BLUE_LEDmed 7
#define GREEN_LEDmed 6

#define RED_LEDlarge 8
#define BLUE_LEDlarge 10
#define GREEN_LEDlarge 9

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

//overall brightness value
int brightness = 255;
//individual brightness values for the red, green and blue LEDs
int gBrightSmall = 0; 
int rBrightSmall = 0;
int bBrightSmall = 0;

int gBright = 0; 
int rBright = 0;
int bBright = 0;

int gBrightMed = 0; 
int rBrightMed = 0;
int bBrightMed = 0;

int gBrightLarge = 0; 
int rBrightLarge = 0;
int bBrightLarge = 0;

int fadeSpeed = 3;

String incomingByte = ""; // for incoming serial data

void setup() {
  //set up pins to output.
  pinMode(buttonPin, INPUT);
  pinMode(GREEN_LEDsmall, OUTPUT);
  pinMode(RED_LEDsmall, OUTPUT);
  pinMode(BLUE_LEDsmall, OUTPUT);
  pinMode(GREEN_LEDmed, OUTPUT);
  pinMode(RED_LEDmed, OUTPUT);
  pinMode(BLUE_LEDmed, OUTPUT);
  pinMode(GREEN_LEDlarge, OUTPUT);
  pinMode(RED_LEDlarge, OUTPUT);
  pinMode(BLUE_LEDlarge, OUTPUT);
  setSmallColor(0,0,0);
  setMedColor(0,0,0);
  setLargeColor(0,0,0);
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
}

void standBy(){
   
    for (int i=0;i<256; i++){
      
      analogWrite(RED_LEDsmall, rBrightSmall);
      rBrightSmall +=1;
      if (gBrightSmall > 0) {
        analogWrite(GREEN_LEDsmall, gBrightSmall);
        gBrightSmall -=1;
      }
      analogWrite(RED_LEDmed, rBrightMed);
      rBrightMed +=1;
      if (gBrightMed > 0) {
        analogWrite(GREEN_LEDmed, gBrightMed);
        gBrightMed -=1;
      }
      analogWrite(RED_LEDlarge, rBrightLarge);
      rBrightLarge +=1;
      if (gBrightLarge > 0) {
        analogWrite(GREEN_LEDlarge, gBrightLarge);
        gBrightLarge -=1;
      }
      
      delay(fadeSpeed);

    }
    for (int i=0;i<256; i++){
      
      analogWrite(BLUE_LEDsmall, bBrightSmall);
      bBrightSmall += 1;
      analogWrite(RED_LEDsmall, rBrightSmall);
      rBrightSmall -=1;
      
      analogWrite(BLUE_LEDmed, bBrightMed);
      bBrightMed += 1;
      analogWrite(RED_LEDmed, rBrightMed);
      rBrightMed -=1;
      analogWrite(BLUE_LEDlarge, bBrightLarge);
      bBrightLarge += 1;
      analogWrite(RED_LEDlarge, rBrightLarge);
      rBrightLarge -=1;
      
      delay(fadeSpeed);
    }  

    for (int i=0;i<256; i++){
      
      analogWrite(GREEN_LEDsmall, gBrightSmall);
      gBrightSmall +=1;
      analogWrite(BLUE_LEDsmall, bBrightSmall);
      bBrightSmall -= 1;
      
      analogWrite(GREEN_LEDmed, gBrightMed);
      gBrightMed +=1;
      analogWrite(BLUE_LEDmed, bBrightMed);
      bBrightMed -= 1;
      analogWrite(GREEN_LEDlarge, gBrightLarge);
      gBrightLarge +=1;
      analogWrite(BLUE_LEDlarge, bBrightLarge);
      bBrightLarge -= 1;
      
      delay(fadeSpeed);
    }  
}


void TurnOff(){
    setSmallColor(0,0,0);
    setMedColor(0,0,0);
    setLargeColor(0,0,0);
}

void TurnOn(int red, int green, int blue){
    setSmallColor(red,green,blue);
    setMedColor(red,green,blue);
    setLargeColor(red,green,blue);
}
void TurnOnTime(int red, int green, int blue, int timeOut){
    setSmallColor(red,green,blue);
    setMedColor(red,green,blue);
    setLargeColor(red,green,blue);
    delay(timeOut);
}
void setSmallColor(int red, int green, int blue) {
    analogWrite(RED_LEDsmall, red);
    analogWrite(GREEN_LEDsmall, green);
    analogWrite(BLUE_LEDsmall, blue);
}

void setMedColor(int red, int green, int blue) {
    analogWrite(RED_LEDmed, red);
    analogWrite(GREEN_LEDmed, green);
    analogWrite(BLUE_LEDmed, blue);
}

void setLargeColor(int red, int green, int blue) {
    analogWrite(RED_LEDlarge, red);
    analogWrite(GREEN_LEDlarge, green);
    analogWrite(BLUE_LEDlarge, blue);
}

void pulse(String color, int speed, int timeOut, String endEvent) {
  if (color.equals("red")) {
    rBright = 255;
    gBright = 0;
    bBright = 0;
  } else if (color.equals("blue")) {
    rBright = 0;
    gBright = 0;
    bBright = 255;
  } else if (color.equals("orange")) {
    rBright = 255;
    gBright = 128;
    bBright = 0;
  } else if (color.equals("white")) {
    rBright = 255;
    gBright = 255;
    bBright = 255;
  } else if (color.equals("green")) {
    rBright = 0;
    gBright = 255;
    bBright = 0;
  } else if (color.equals("yellow")) {
    rBright = 255;
    gBright = 255;
    bBright = 0;
  }
  for (int i = timeOut; i > 0; i--) {
    setSmallColor(rBright, gBright, bBright);
    delay(speed);
    setMedColor(rBright, gBright, bBright);
    delay(speed);
    setLargeColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    delay(speed);
  }
}
void sparkle(String color, int speed, int timeOut, String endEvent) {
  if (color.equals("red")) {
    rBright = 255;
    gBright = 0;
    bBright = 0;
  } else if (color.equals("blue")) {
    rBright = 0;
    gBright = 0;
    bBright = 255;
  } else if (color.equals("orange")) {
    rBright = 255;
    gBright = 128;
    bBright = 0;
  } else if (color.equals("white")) {
    rBright = 255;
    gBright = 255;
    bBright = 255;
  } else if (color.equals("green")) {
    rBright = 0;
    gBright = 255;
    bBright = 0;
  } else if (color.equals("yellow")) {
    rBright = 255;
    gBright = 255;
    bBright = 0;
  }
  for (int i = timeOut; i > 0; i--) {
    setSmallColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    setLargeColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    setSmallColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    setLargeColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    setSmallColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    delay(speed);
  }
}

void blink(String color, int speed, int timeOut, String endEvent) {
  if (color.equals("red")) {
    rBright = 255;
    gBright = 0;
    bBright = 0;
  } else if (color.equals("blue")) {
    rBright = 0;
    gBright = 0;
    bBright = 255;
  } else if (color.equals("orange")) {
    rBright = 255;
    gBright = 128;
    bBright = 0;
  } else if (color.equals("white")) {
    rBright = 255;
    gBright = 255;
    bBright = 255;
  } else if (color.equals("green")) {
    rBright = 0;
    gBright = 255;
    bBright = 0;
  } else if (color.equals("yellow")) {
    rBright = 255;
    gBright = 255;
    bBright = 0;
  }
  for (int i = timeOut; i > 0; i--) {
    setSmallColor(rBright, gBright, bBright);
    setMedColor(rBright, gBright, bBright);
    setLargeColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    delay(speed);
    setSmallColor(rBright, gBright, bBright);
    setMedColor(rBright, gBright, bBright);
    setLargeColor(rBright, gBright, bBright);
    delay(speed);
    TurnOff();
    delay(speed);
  }
}

void loop(){
  buttonState = digitalRead(buttonPin);
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
//  if (buttonState == HIGH) {
//    TurnOn(255,0,0);
//    Serial.println("RED");
//  } else {
//    //TurnOn(255,255,255);
//    listen();
//  }
//  standBy();
  listen();
}

void listen() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.readStringUntil('\n');
    Serial.println("I got: " + incomingByte + " " + incomingByte.substring(1, incomingByte.indexOf(",")) + " " + incomingByte.substring(incomingByte.indexOf(",")+2, incomingByte.indexOf(")")-7) + " " + incomingByte.substring(incomingByte.indexOf(")")-5, incomingByte.indexOf(")")));
    
    TurnOn(incomingByte.substring(1, incomingByte.indexOf(",")).toInt(), incomingByte.substring(incomingByte.indexOf(",")+2, incomingByte.indexOf(")")-7).toInt(), incomingByte.substring(incomingByte.indexOf(")")-5, incomingByte.indexOf(")")).toInt());
    // if (incomingByte.substring(0,1).equals("1")) {
    //   if (incomingByte.substring(1,2).equals("1")) {
    //     Serial.println("Light");
    //   } else {
    //     String color = incomingByte.substring(incomingByte.indexOf("!")+1,incomingByte.indexOf("!!"));
    //     int speed = incomingByte.substring(incomingByte.indexOf("!!")+2,incomingByte.indexOf("!!!")).toInt();
    //     int timeOut = incomingByte.substring(incomingByte.indexOf("!!!")+3,incomingByte.indexOf("!!!!")).toInt();
    //     String endEvent = incomingByte.substring(incomingByte.indexOf("!!!!")+4);
    //     if (incomingByte.substring(2,3).equals("1")) {
    //       if (color.equals("red")) {
    //         rBright = 255;
    //         gBright = 0;
    //         bBright = 0;
    //       } else if (color.equals("blue")) {
    //         rBright = 0;
    //         gBright = 0;
    //         bBright = 255;
    //       } else if (color.equals("orange")) {
    //         rBright = 255;
    //         gBright = 128;
    //         bBright = 0;
    //       } else if (color.equals("white")) {
    //         rBright = 255;
    //         gBright = 255;
    //         bBright = 255;
    //       } else if (color.equals("green")) {
    //         rBright = 0;
    //         gBright = 255;
    //         bBright = 0;
    //       } else if (color.equals("yellow")) {
    //         rBright = 255;
    //         gBright = 255;
    //         bBright = 0;
    //       }
    //       TurnOnTime(rBright, gBright, bBright, timeOut);
    //     } else if (incomingByte.substring(2,3).equals("2")) {
    //       pulse(color, speed, timeOut, endEvent);
    //     } else if (incomingByte.substring(2,3).equals("3")) {
    //       sparkle(color, speed, timeOut, endEvent);
    //     } else if (incomingByte.substring(2,3).equals("4")) {
    //       blink(color, speed, timeOut, endEvent);
    //     } else {
    //       TurnOff();
    //     }
    //   }
    // } else {
    //   TurnOn(255, 0, 0)
    // }
    } // else {
//    standBy();
//  }
  // else {
  //   standBy();
  // }// 102!red!!200!!!3!!!!sparkle
}
