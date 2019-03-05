#include <Arduino.h>
#line 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
#line 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
#include "settings.h"

#line 3 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void setup();
#line 30 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void loop();
#line 44 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void mvmtFORWARD(int distance);
#line 75 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void mvmtRIGHT(int angle);
#line 113 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void mvmtLEFT(int angle);
#line 152 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void mvmtSTOP();
#line 161 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void PIDControl(int *setSpdR, int *setSpdL, int kP, int kI, int kD, int dr);
#line 196 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
int angleToTicks(long angle);
#line 204 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
int blockToTicks(int blocks);
#line 220 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void resetMCounters();
#line 239 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void pciSetup(byte pin);
#line 248 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void usbReceiveMSG(RCVDMessage *MSG_Buffer);
#line 292 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void usbSendMSG(SENDMessage *MSG_Buffer);
#line 308 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void rpiCommunication();
#line 349 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void stringCommands(char commands[], int len);
#line 3 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v02\\fyp_ard_fw_v01.ino"
void setup()
{
    Serial.begin(9600);
    //D Serial.println("Robot: Hello World!");
    md.init();

    //Initialise Motor Encoder Pins, digitalWrite high to enable PullUp Resistors
    pinMode(m1EncA, INPUT);
    pinMode(m1EncB, INPUT);
    pinMode(m2EncA, INPUT);
    pinMode(m2EncB, INPUT);

    //Innitializes the Motor Encoders for Interrupts
    pciSetup(m1EncA);
    pciSetup(m1EncB);
    pciSetup(m2EncA);
    pciSetup(m2EncB);

    delay(1000);
    D Serial.println("Initializations Done");

    memset(&msgRCVD, 0, sizeof(RCVDMessage));
    memset(&msgSEND, 0, sizeof(SENDMessage));

    delay(1000);
}

void loop()
{
    Serial.println(sizeof(commands));
    if (commands[0] != '0')
    {
        stringCommands(commands, sizeof(commands) / sizeof(char));
    }
    else
    {
        rpiCommunication();
    }
}

//------------Functions for robot movements------------//
void mvmtFORWARD(int distance)
{
    long lastTime = micros();
    //int setSpdR = 400; //400;                //Original: 300
    //int setSpdL = 400; //400;                //Original: 300
    int colCounter = 0;
    resetMCounters();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;

    md.setSpeeds(setSpdR, setSpdL);
    lastTime = millis();

    while (mCounter[0] < distance && mCounter[1] < distance)
    {
        if (millis() - lastTime > 100)
        {
            PIDControl(&setSpdR, &setSpdL, 40, 0, 40, 0); //By block 40, 0, 80, 0
            lastTime = millis();
            //setSpdR = setSpdR - 1;
            //setSpdL = setSpdL + 1;
            md.setSpeeds(setSpdR, setSpdL);
        }
    }

    //mvmtSTOP();
    //delay(100);
}

void mvmtRIGHT(int angle)
{
    int setSpdR = -400; //Right motor
    int setSpdL = 400;  //Left motor
    long lastTime = millis();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;
    resetMCounters();

    md.setSpeeds(setSpdR, setSpdL);
    delay(50);
    while (mCounter[0] < angle - 200 && mCounter[1] < angle - 200)
    {
        if (millis() - lastTime > 100)
        {
            PIDControl(&setSpdR, &setSpdL, 150, 6, 15, 1);
            lastTime = millis();
            md.setSpeeds(setSpdR, setSpdL);
        }
    }
    int i = 0;
    lastTime = micros();
    while (mCounter[0] < angle && mCounter[1] < angle)
    {
        if (micros() - lastTime > 50)
        {
            md.setSpeeds(setSpdR + i, setSpdL - i);
            i++;
            if (i > 100)
                i = 100;
            lastTime = micros();
        }
    }
    md.setBrakes(400, 400);
}

void mvmtLEFT(int angle)
{
    int setSpdR = 400;  //Right motor
    int setSpdL = -400; //Left motor
    long lastTime = millis();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;
    resetMCounters();

    md.setSpeeds(setSpdR, setSpdL);
    delay(50);

    while (mCounter[0] < angle - 200 && mCounter[1] < angle - 200)
    {
        if (millis() - lastTime > 100)
        {
            PIDControl(&setSpdR, &setSpdL, 150, 6, 15, -1);
            lastTime = millis();
            md.setSpeeds(setSpdR, setSpdL);
        }
    }
    int i = 0;
    lastTime = micros();
    while (mCounter[0] < angle && mCounter[1] < angle)
    {
        if (micros() - lastTime > 50)
        {
            md.setSpeeds(setSpdR - i, setSpdL + i);
            i++;
            if (i > 100)
                i = 100;
            lastTime = micros();
        }
    }
    md.setBrakes(400, 400);
}

void mvmtSTOP()
{
    setSpdL = 0;
    setSpdR = 0;
    resetMCounters();
    md.setBrakes(0, 0);
}

//Direction(dr): -1 = left, 0 = straight, 1 = right
void PIDControl(int *setSpdR, int *setSpdL, int kP, int kI, int kD, int dr)
{
    int adjustment;
    int error = (mCounter[1] - lastTicks[1]) - (mCounter[0] - lastTicks[0]); //0 = right motor, 1 = left motor, lesser tick time mean faster
    int errorRate = error - lastError;
    lastError = error;
    lastTicks[0] = mCounter[0];
    lastTicks[1] = mCounter[1];
    //totalErrors += 2;
    //totalErrors = 0;
    //   totalErrors += error             ;                                           //Add up total number of errors (for Ki)
    //  if (error != 0) {                                                           //if error exists
    adjustment = ((kP * error) - (kI * totalErrors) + (kD * errorRate)) / 100;

    if (dr == 1 || dr == -1)
    {
        *setSpdR += -adjustment * dr;
        *setSpdL -= adjustment * dr;
    }
    else
    {
        *setSpdR += adjustment;
        *setSpdL -= adjustment;

        if (*setSpdR > 400)
        {
            *setSpdR = 400;
        }
        if (*setSpdL > 400)
        {
            *setSpdL = 400;
        }
    }
}

int angleToTicks(long angle)
{
    if (angle == 90)
        return 16800 * angle / 1000;
    else
        return (17280 * angle / 1000);
}

int blockToTicks(int blocks)
{
    return 1192 * blocks; //1192 * blocks;
}

//------------Functions for IR Sensors------------//
/*
void scanFORWARD()
{
    int val = mfwdIrVal.distance(); // Middle
    delay(2);
    D Serial << "FORWARD: () Mid: " << val << endl;
}
*/

//------------Functions for Motors------------//
void resetMCounters()
{
    mCounter[0] = 0;
    mCounter[1] = 0;
}

//ISR for Motor 1 (Right) Encoders
ISR(PCINT2_vect)
{
    mCounter[0]++;
}

//ISR for Motor 2 (Left) Encoders
ISR(PCINT0_vect)
{
    mCounter[1]++;
}

//Standard function to enable interrupts on any pins
void pciSetup(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit(digitalPinToPCMSKbit(pin)); // enable pin
    PCIFR |= bit(digitalPinToPCICRbit(pin));                   // clear any outstanding interrupt
    PCICR |= bit(digitalPinToPCICRbit(pin));                   // enable interrupt for the group
}

//------------Functions for communications------------//

void usbReceiveMSG(RCVDMessage *MSG_Buffer)
{
    static uint8_t tempBuffer[MAX_BYTE_DATA];
    static uint8_t tempByte = 0;
    static int index = 0;
    static boolean recieving = false;

    while (Serial.available() > 0 && index < MAX_BYTE_DATA + 1) //Total index + STOP byte
    {
        tempByte = Serial.read();
        //Serial.println(tempByte);

        if (recieving == true)
        {
            if (tempByte != STOP)
            {
                tempBuffer[index] = tempByte;
                index++;
            }

            else
            {
                recieving = false;
                index = 0;

                MSG_Buffer->type = tempBuffer[0];
                MSG_Buffer->id = tempBuffer[1];
                MSG_Buffer->distance = ((uint16_t)tempBuffer[2] << 7) | tempBuffer[3];
                MSG_Buffer->motorspeed = ((uint16_t)tempBuffer[4] << 7) | tempBuffer[5];
                MSG_Buffer->motorangle = ((uint16_t)tempBuffer[6] << 7) | tempBuffer[7];

                digitalWrite(13, HIGH);
            }
        }

        else if (tempByte == START)
        {
            recieving = true;
        }

        delay(5);
    }
}

void usbSendMSG(SENDMessage *MSG_Buffer)
{
    byte writebuff[] = {START, MSG_Buffer->type, MSG_Buffer->id, MSG_Buffer->state, highByte(MSG_Buffer->frontDistance), lowByte(MSG_Buffer->frontDistance), highByte(MSG_Buffer->bearings), lowByte(MSG_Buffer->bearings), STOP};
    Serial.write(writebuff, 9);
    //Serial << char(START) << char(MSG_Buffer->type) << char(MSG_Buffer->id) << char(MSG_Buffer->state) << char(STOP);
    /* Serial.println("--SENDMESSAGE--");
    Serial.println(START);
    Serial.println(MSG_Buffer->type);
    Serial.println(MSG_Buffer->id);
    Serial.println(MSG_Buffer->state);
    Serial.println(MSG_Buffer->frontDistance);
    Serial.println(MSG_Buffer->bearings);
    Serial.println(STOP);
    Serial.println("----"); */
}

void rpiCommunication()
{
    usbReceiveMSG(&msgRCVD);           //Process incoming message packet
    char control = char(msgRCVD.type); //Then assign to a variable to control

    switch (control)
    {
    case 'F':
        //goFORWARD(blockToTicks(3));
        msgSEND.type = 'F';
        msgSEND.state = 'W';
        usbSendMSG(&msgSEND);
        break;

    case 'L':
        //goLEFT(angleToTicks(90));
        msgSEND.type = 'L';
        msgSEND.state = 'A';
        usbSendMSG(&msgSEND);
        break;

    case 'R':
        //goRIGHT(angleToTicks(90));
        msgSEND.type = 'R';
        msgSEND.state = 'D';
        usbSendMSG(&msgSEND);
        break;

    case 'S':
        //stop();
        msgSEND.type = 'S';
        msgSEND.state = 'S';
        usbSendMSG(&msgSEND);
        break;
    }

    memset(&msgRCVD, 0, sizeof(RCVDMessage)); //Clear received message
    //usbSendMSG(&msgSEND);
    delay(RPI_DELAY);
}

void stringCommands(char commands[], int len)
{
    static int calCounter = 0;
    static int x;

    Serial.println(sizeof(commands));

    switch (commands[x])
    {
    case 'f':
        if (setSpdL != 0 && setSpdR != 0)
        {
            setSpdL = 400;
            setSpdR = 400;
        }
        //mvmtFORWARD(blockToTicks(1));
        break;

    case 'l':
        break;

    case 'r':
        break;

    case 's':
        mvmtSTOP();
        break;

    default:
        mvmtSTOP();
        break;
    }

    delay(ARD_DELAY);

    if (x <= len)
    {
        x++;
    }
}

