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
int Motor1Pin1 = 30;
int Motor1Pin2 = 31;
int Motor1Enable = 44;

int Motor5Pin1 = 33;              
int Motor5Pin2 = 32;
int Motor5Enable = 45;

int Motor3Pin1 = 36;              
int Motor3Pin2 = 37;
int Motor3Enable = 7;

int Motor4Pin1 = 40;              
int Motor4Pin2 = 41;
int Motor4Enable = 9;

int Motor2Pin1 = 39;              
int Motor2Pin2 = 38;
int Motor2Enable = 8;

int Motor6Pin1 = 34;              
int Motor6Pin2 = 35;
int Motor6Enable = 46;

int i=0;
//Other pins
int lightPin = 6;


void setup() {
  Serial.begin(9600);           //Turn on Serial Port
  Ethernet.begin(mac, ip);      //Initialize Ethernet
  Udp.begin(localPort);         //Initialize Udp
  delay(1500);                  //Pause for effect

  pinMode(lightPin, OUTPUT);
}

void loop() {
  i=0;
  while(Udp.parsePacket() == 0) {
    i++;
  }
  
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
  


  runMotor(Motor1Power, Motor1Pin1, Motor1Pin2, Motor1Enable);
  runMotor(Motor2Power, Motor2Pin1, Motor2Pin2, Motor2Enable);
  runMotor(Motor3Power, Motor3Pin1, Motor3Pin2, Motor3Enable);
  runMotor(Motor4Power, Motor4Pin1, Motor4Pin2, Motor4Enable);
  runMotor(Motor5Power, Motor5Pin1, Motor5Pin2, Motor5Enable);
  runMotor(Motor6Power, Motor6Pin1, Motor6Pin2, Motor6Enable);
  analogWrite(lightPin, brightness);

  
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(i);
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
