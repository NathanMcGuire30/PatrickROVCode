#include <Servo.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE};       //Assign a mac address
IPAddress ip(172, 16, 0, 3);                              //Assign my IP adress
unsigned int localPort = 5000;                            //Assign a Port to talk over
char packetBuffer[1024];                                  //Increase if strings are cut off
String datReq;                                            //String for data
int packetSize;                                           //Size of Packet
EthernetUDP Udp;                                          //Define UDP Object

//Motor ports
int Motor1Pin1 = 40;
int Motor1Pin2 = 42;
int Motor1Enable = 4;

int Motor2Pin1 = 41;              
int Motor2Pin2 = 43;
int Motor2Enable = 5;

int Motor3Pin1 = 32;              
int Motor3Pin2 = 34;
int Motor3Enable = 7;

int Motor4Pin1 = 33;              
int Motor4Pin2 = 35;
int Motor4Enable = 6;

int Motor5Pin1 = 36;              
int Motor5Pin2 = 38;
int Motor5Enable = 9;

int Motor6Pin1 = 37;              
int Motor6Pin2 = 39;
int Motor6Enable = 8;

Servo camPitch;

int i=0;
int loopTime = 0;
//Other pins
int lightPin = 3;
int battPin = 0;

int lastMsgTime = 0;
bool hasComms = false;


void setup() {
  Serial.begin(9600);           //Turn on Serial Port
  delay(1000);
  Ethernet.begin(mac, ip);      //Initialize Ethernet
  Udp.begin(localPort);         //Initialize Udp
  delay(1500);                  //Pause for effect

  pinMode(lightPin, OUTPUT);
  blinkLights();

  camPitch.attach(44);
}

void loop() {
  //Check for data  
  while(Udp.parsePacket() == 0) {           //While loop runs untill we get comms
    //Feedback controll goes here
    loopTime = millis() - lastMsgTime;
    delay(1);
    if (loopTime >= 2000) {				//Its been a while since the last command
      stopMotors();
      hasComms = false;
    }
  }

  //This all happens once we get comms
  if(hasComms == false) {         //This happens the first time we get comms
    blinkLights();
    hasComms = true;
  }

  double battVoltage = analogRead(battPin);
  battVoltage /= 204.6;
  battVoltage *= 4.0;
  //Serial.println(battVoltage);
  
  lastMsgTime = millis();			//Reset time of message
  Udp.read(packetBuffer, 1024);     //Reading the data request on the Udp
  String datReq(packetBuffer);                        //Convert packetBuffer array to string datReq

  //break string into actuall values
  int Motor1Power = getValue(datReq, ',', 0).toInt();       
  int Motor2Power = getValue(datReq, ',', 1).toInt();      
  int Motor3Power = getValue(datReq, ',', 2).toInt();       
  int Motor4Power = getValue(datReq, ',', 3).toInt();      
  int Motor5Power = getValue(datReq, ',', 4).toInt();       
  int Motor6Power = getValue(datReq, ',', 5).toInt();       
  int brightness = getValue(datReq, ',', 6).toInt();        //Light
  int cameraAngle = getValue(datReq, ',', 7).toInt();       //Camera pitch
  
  runMotor(Motor1Power, Motor1Pin1, Motor1Pin2, Motor1Enable);
  runMotor(Motor2Power, Motor2Pin1, Motor2Pin2, Motor2Enable);
  runMotor(Motor3Power, Motor3Pin1, Motor3Pin2, Motor3Enable);
  runMotor(Motor4Power, Motor4Pin1, Motor4Pin2, Motor4Enable);
  runMotor(Motor5Power, Motor5Pin1, Motor5Pin2, Motor5Enable);
  runMotor(Motor6Power, Motor6Pin1, Motor6Pin2, Motor6Enable);
  analogWrite(lightPin, brightness);
  camPitch.write(cameraAngle);
  //Serial.println(cameraAngle);

  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.print(String(battVoltage) + "'" + String(loopTime));
  Udp.endPacket();   memset(packetBuffer, 0, 1024);
}

/*
 * Commands to run motors correctly
 * Takes input from -255 to 255
 */
void runMotor(int power, int pin1, int pin2, int enablePin) {
  if (power >= 0) {                 //Forwards
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    analogWrite(enablePin, power);
  } else {                          //Backwards
    power *=-1;
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
    analogWrite(enablePin, power);
  }
}

void stopMotors() {
  runMotor(0, Motor1Pin1, Motor1Pin2, Motor1Enable);
  runMotor(0, Motor2Pin1, Motor2Pin2, Motor2Enable);
  runMotor(0, Motor3Pin1, Motor3Pin2, Motor3Enable);
  runMotor(0, Motor4Pin1, Motor4Pin2, Motor4Enable);
  runMotor(0, Motor5Pin1, Motor5Pin2, Motor5Enable);
  runMotor(0, Motor6Pin1, Motor6Pin2, Motor6Enable);
}


//Blinks lights on startup
void blinkLights() {
  for(int i=0; i<5; i++){
    digitalWrite(lightPin, HIGH);
    delay(100);
    digitalWrite(lightPin, LOW);
    delay(100);
  }
}


/*
 * Method that parses a string at a specific index of a charecter
 * Don't change or touch at all, won't change how the robot drives.
 * Seriously, editing this will break the program
 * JUST DON'T TOUCH THIS.  OK?
 * 
 * Disclaimer: I did not write this, I coppied it off the internet, and it works for now
 */
String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {0, -1};
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
