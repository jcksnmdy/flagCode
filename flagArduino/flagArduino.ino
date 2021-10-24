//Code created by Ian Buckley for an article on makeuseof.com

#include<Wire.h>
const int MPU=0x68; 
int16_t GyZ,start;
int count = 1;
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
String smallCode = ""; // for incoming serial data
String medCode = ""; // for incoming serial data
String largeCode = ""; // for incoming serial data

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
  TurnOn(0, 0, 0);
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
  Wire.write(0);   
  Wire.endTransmission(true);
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  delay(1333);
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
    analogWrite(GREEN_LEDsmall, (int)(green*0.97));
    analogWrite(RED_LEDsmall, (int)(red*0.97));
    analogWrite(BLUE_LEDsmall, (int)(blue*0.97));
    //Serial.println(String((int)(red*0.86)) + ", " + String((int)(green*0.94)) + ", " + String((int)(blue)));
}

void setMedColor(int red, int green, int blue) {
    analogWrite(RED_LEDmed, (int)(red*0.97));
    analogWrite(GREEN_LEDmed, (int)(green*0.97));
    analogWrite(BLUE_LEDmed, (int)(blue*0.97));
    //Serial.println(String((int)(red*0.86)) + ", " + String((int)(green*0.94)) + ", " + String((int)(blue)));
}

void setLargeColor(int red, int green, int blue) {
    analogWrite(RED_LEDlarge, (int)(red*0.97));
    analogWrite(GREEN_LEDlarge, (int)(green*0.97));
    analogWrite(BLUE_LEDlarge, (int)(blue*0.97));
    //Serial.println(String((int)(red*0.86)) + ", " + String((int)(green*0.94)) + ", " + String((int)(blue)));
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
    rBright = 240;
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
    setMedColor(rBright, gBright, bBright);
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
boolean listening = false;
void loop(){
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,12,true);  
  if (count == 1) {
     start=Wire.read()<<8|Wire.read(); 
  }
  count+=1;
  GyZ=Wire.read()<<8|Wire.read(); 
  //listen();
  //TurnOn(255,35,0);
  if (Serial.available() > 0) {
    Serial.println(listen());
  } else if(start+1500<GyZ) {
    if (listening) {
      Serial.println("HIT");
    }
    delay(500);
    sparkle("white", 60, 3, "idk");
    Serial.println("not");
  } 
    //Serial.println(listen());
    //Serial.println("");
    //TurnOn(255,0,0);
    //Serial.println("not");(128.0, 128.0, 128.0)(128.0, 128.0, 128.0)(128.0, 128.0, 128.0)
  
}

String listen() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.readStringUntil('\n');
    if (incomingByte.indexOf("smack")>=0){
      sparkle("white", 630, 3,"idk");
      delay(2000);
      return "blinked";
    } else if (incomingByte.indexOf("prepareSong")>=0){
      pulse("white", 1000, 3, "LOL");
      delay(10000)
      return "Preparing";
    } else if (incomingByte.indexOf("notMode")>=0){
      listening = false;
      return "notWriting";
    }  else if (incomingByte.indexOf("modeing")>=0){
      listening = true;
      return "Writing";
    } else {
    smallCode = incomingByte.substring(0, incomingByte.indexOf(")(")+1);
    medCode = incomingByte.substring(incomingByte.indexOf(")(")+1, incomingByte.indexOf(")(", 23)+1);
    largeCode = incomingByte.substring(incomingByte.indexOf(")(", 23)+1, incomingByte.indexOf(")", 43)+1);
    //Serial.println("I got: " + incomingByte + " " + incomingByte.substring(1, incomingByte.indexOf(",")) + " " + incomingByte.substring(incomingByte.indexOf(",")+2, incomingByte.indexOf(",", 7)) + " " + incomingByte.substring(incomingByte.indexOf(",", 7)+2, incomingByte.indexOf(")")));

    setSmallColor(smallCode.substring(1, smallCode.indexOf(",")).toInt(), smallCode.substring(smallCode.indexOf(",")+2, smallCode.indexOf(",", 7)).toInt(), smallCode.substring(smallCode.indexOf(",", 7)+2, smallCode.indexOf(")")).toInt());
    setMedColor(medCode.substring(1, medCode.indexOf(",")).toInt(), medCode.substring(medCode.indexOf(",")+2, medCode.indexOf(",", 7)).toInt(), medCode.substring(medCode.indexOf(",", 7)+2, medCode.indexOf(")")).toInt());
    setLargeColor(largeCode.substring(1, largeCode.indexOf(",")).toInt(), largeCode.substring(largeCode.indexOf(",")+2, largeCode.indexOf(",", 7)).toInt(), largeCode.substring(largeCode.indexOf(",", 7)+2, largeCode.indexOf(")")).toInt());
    
    //return "(" + String(smallCode.substring(1, smallCode.indexOf(",")).toInt()) + ", " + String(smallCode.substring(smallCode.indexOf(",")+2, smallCode.indexOf(",", 7)).toInt()) + ", " + String(smallCode.substring(smallCode.indexOf(",", 7)+2, smallCode.indexOf(")")).toInt()) + ")(" + String(medCode.substring(1, medCode.indexOf(",")).toInt()) + ", " + String(medCode.substring(medCode.indexOf(",")+2, medCode.indexOf(",", 7)).toInt()) + ", " + String(medCode.substring(medCode.indexOf(",", 7)+2, medCode.indexOf(")")).toInt()) + ")(" + String(largeCode.substring(1, largeCode.indexOf(",")).toInt()) + ", " + String(largeCode.substring(largeCode.indexOf(",")+2, largeCode.indexOf(",", 7)).toInt()) + ", " + String(largeCode.substring(largeCode.indexOf(",", 7)+2, largeCode.indexOf(")")).toInt()) + ")";
    return smallCode + " " + medCode + " " + largeCode;
    }
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
    }// else {
//    standBy();
//  }
  // else {
  //   standBy();
  // }// 102!red!!200!!!3!!!!sparkle
}
