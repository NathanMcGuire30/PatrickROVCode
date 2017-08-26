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
int Motor1Pin1 = 30;              //Yellow
int Motor1Pin2 = 31;
int Motor1Enable = 44;

int Motor2Pin1 = 33;              //Blue
int Motor2Pin2 = 32;
int Motor2Enable = 45;

int Motor3Pin1 = 36;              //White
int Motor3Pin2 = 37;
int Motor3Enable = 7;

int Motor4Pin1 = 40;              //Orange
int Motor4Pin2 = 41;
int Motor4Enable = 9;

int Motor5Pin1 = 39;              //Brown
int Motor5Pin2 = 38;
int Motor5Enable = 8;

int Motor6Pin1 = 34;              //Green
int Motor6Pin2 = 35;
int Motor6Enable = 46;

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
  packetSize = Udp.parsePacket();     //Read the packetSize

  if (packetSize > 0) {               //Check to see if a request is present
    Udp.read(packetBuffer, 1024);     //Reading the data request on the Udp
    String datReq(packetBuffer);                        //Convert packetBuffer array to string datReq

    //break string into actuall values
    int Motor1Power = getValue(datReq, ',', 0).toInt();       //Front Left
    int Motor2Power = getValue(datReq, ',', 1).toInt();       //Front Right
    int Motor3Power = getValue(datReq, ',', 2).toInt();       //Rear Left
    int Motor4Power = getValue(datReq, ',', 3).toInt();       //Rear Right
    int Motor5Power = getValue(datReq, ',', 4).toInt();       //Left Vertical
    int Motor6Power = getValue(datReq, ',', 5).toInt();       //Right Vertical
    int brightness = getValue(datReq, ',', 6).toInt();        //Light
    

    //Serial.println(datReq);

    runMotor(Motor1Power, Motor1Pin1, Motor1Pin2, Motor1Enable);
    runMotor(Motor2Power, Motor2Pin1, Motor2Pin2, Motor2Enable);
    runMotor(Motor3Power, Motor3Pin1, Motor3Pin2, Motor3Enable);
    runMotor(Motor4Power, Motor4Pin1, Motor4Pin2, Motor4Enable);
    runMotor(Motor5Power, Motor5Pin1, Motor5Pin2, Motor5Enable);
    runMotor(Motor6Power, Motor6Pin1, Motor6Pin2, Motor6Enable);
    analogWrite(lightPin, brightness);
  }
  memset(packetBuffer, 0, 1024);
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
