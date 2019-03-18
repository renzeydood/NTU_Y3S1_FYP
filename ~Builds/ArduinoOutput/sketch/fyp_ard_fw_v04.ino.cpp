#include <Arduino.h>
#line 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
#line 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
#include "settings.h"

#line 3 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void setup();
#line 41 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void loop();
#line 61 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtFORWARD();
#line 90 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtRIGHTStatic(int angle);
#line 117 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtLEFTStatic(int angle);
#line 144 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtSTOP();
#line 156 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtRIGHT(int angle);
#line 166 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void mvmtLEFT(int angle);
#line 177 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void PIDControl(int *setSpdR, int *setSpdL, int kP, int kI, int kD, int dr);
#line 212 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
int angleToTicks(long angle);
#line 220 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
int blockToTicks(int blocks);
#line 225 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void spdAdjustment();
#line 233 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
int scanFORWARD();
#line 242 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void resetMCounters();
#line 261 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void pciSetup(byte pin);
#line 270 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void usbReceiveMSG(RCVDMessage *MSG_Buffer);
#line 314 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void usbSendMSG(SENDMessage *MSG_Buffer);
#line 330 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void rpiCommunication(char control);
#line 432 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void stringCommands(char commands[], int len);
#line 3 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\~Builds\\fyp_ard_fw_v04\\fyp_ard_fw_v04.ino"
void setup()
{
    Serial.begin(19200);
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

    memset(&msgRCVD, 0, sizeof(RCVDMessage));
    memset(&msgSEND, 0, sizeof(SENDMessage));

    delay(500);

    /*     while (1)
    {
        usbReceiveMSG(&msgRCVD);
        if (msgRCVD.type == 'A')
        {
            msgSEND.type = 'O';
            usbSendMSG(&msgSEND);
            break;
        }
        msgSEND.type = 'I';
        usbSendMSG(&msgSEND);
    } */

    D_STREAM("Initializations done!");
}

void loop()
{
    if (commands[0] != '0')
    {
        stringCommands(commands, sizeof(commands) / sizeof(char));
    }

    else
    {
        //Wait for start event
        usbReceiveMSG(&msgRCVD);     //Process incoming message packet
        char c = char(msgRCVD.type); //Then assign to a variable to control
        D_STREAM(c);
        rpiCommunication(c);
        //memset(&msgRCVD, 0, sizeof(RCVDMessage)); //Clear received message
        delay(RPI_DELAY);
    }
}

//------------Functions for robot movements------------//
void mvmtFORWARD()
{
    long lastTime = micros();
    resetMCounters();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;

    if (setSpdL == 0 && setSpdR == 0)
    {
        setSpdL = MAXSPEED_L;
        setSpdR = MAXSPEED_R;
    }

    md.setSpeeds(setSpdR, setSpdL);
    lastTime = millis();

    //while (mCounter[0] < distance && mCounter[1] < distance)
    //{
    if (millis() - lastTime > 80)
    {
        PIDControl(&setSpdR, &setSpdL, 350, 200, 180, 0); //By block 40, 0, 80, 0
        lastTime = millis();
        md.setSpeeds(setSpdR, setSpdL);
    }
    //}
}

void mvmtRIGHTStatic(int angle)
{
    int setSpdRi = -MAXSPEED_R; //Right motor
    int setSpdLi = MAXSPEED_L;  //Left motor
    long lastTime = millis();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;
    resetMCounters();

    md.setSpeeds(setSpdRi, setSpdLi);
    delay(50);

    while (mCounter[0] < angle && mCounter[1] < angle)
    {
        if (millis() - lastTime > 100)
        {
            PIDControl(&setSpdRi, &setSpdLi, 150, 6, 15, 1);
            lastTime = millis();
            md.setSpeeds(setSpdRi, setSpdLi);
        }
    }

    md.setBrakes(400, 400);
}

void mvmtLEFTStatic(int angle)
{
    int setSpdRi = MAXSPEED_R;  //Right motor
    int setSpdLi = -MAXSPEED_L; //Left motor
    long lastTime = millis();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;
    resetMCounters();

    md.setSpeeds(setSpdRi, setSpdLi);
    delay(50);

    while (mCounter[0] < angle && mCounter[1] < angle)
    {
        if (millis() - lastTime > 100)
        {
            PIDControl(&setSpdRi, &setSpdLi, 150, 6, 15, -1);
            lastTime = millis();
            md.setSpeeds(setSpdRi, setSpdLi);
        }
    }

    md.setBrakes(400, 400);
}

void mvmtSTOP()
{
    setSpdL = 0;
    setSpdR = 0;
    resetMCounters();
    md.setBrakes(400, 400);
    //md.setM2Brake(400);
    delay(30);
    //md.setM1Brake(400);
    //delay(2000);
}

void mvmtRIGHT(int angle)
{
    md.setM1Brake(400);
    resetMCounters();
    while (mCounter[1] < (3012 + turnOffset))
    {
        md.setM2Speed(setSpdL);
    }
}

void mvmtLEFT(int angle)
{
    md.setM2Brake(400);
    resetMCounters();
    while (mCounter[0] < (3012 + turnOffset))
    {
        md.setM1Speed(setSpdR);
    }
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
        return (16800 * angle / 1000) + turnOffsetStatic;
    else
        return (17280 * angle / 1000);
}

int blockToTicks(int blocks)
{
    return 1192 * blocks; //1192 * blocks;
}

void spdAdjustment()
{
    int speedRate = msgRCVD.motorspeed;
    setSpdL = ((MAXSPEED_L * speedRate) / 100);
    setSpdR = ((MAXSPEED_R * speedRate) / 100);
}

//------------Functions for IR Sensors------------//
int scanFORWARD()
{
    int val = mfwdIrVal.distance(); // Middle
    delay(2);
    D_STREAM("FORWARD: () Mid: " << val);
    return val;
}

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

    while (Serial.available() > 0) //Total index + STOP byte
    {
        tempByte = Serial.read();
        D_STREAM(tempByte);

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
                D_STREAM("Inside Serialread: " << MSG_Buffer->type);
                MSG_Buffer->type = tempBuffer[0];
                MSG_Buffer->id = tempBuffer[1];
                MSG_Buffer->distance = ((uint16_t)tempBuffer[2] << 7) | tempBuffer[3];
                MSG_Buffer->motorspeed = ((uint16_t)tempBuffer[4] << 7) | tempBuffer[5];
                MSG_Buffer->motorangle = ((uint16_t)tempBuffer[6] << 7) | tempBuffer[7];
                tempByte = 0;
                memset(tempBuffer, 0, sizeof(tempBuffer));
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
    D_STREAM("--SENDMESSAGE--");
    D_STREAM(START);
    D_STREAM(MSG_Buffer->type);
    D_STREAM(MSG_Buffer->id);
    D_STREAM(MSG_Buffer->state);
    D_STREAM(MSG_Buffer->frontDistance);
    D_STREAM(MSG_Buffer->bearings);
    D_STREAM(STOP);
    D_STREAM("----");
}

void rpiCommunication(char control)
{
    int irfront = scanFORWARD();
    D_STREAM("Sensor value: " << irfront);

    switch (control)
    {
    case 'F':
        if (irfront > 90)
        {
            mvmtFORWARD();
            D_STREAM("Moving forward!");
            if (msgSEND.type != 'F')
            {
                msgSEND.type = 'F';
                msgSEND.state = 'W';
                msgSEND.frontDistance = irfront;
                msgSEND.id++;
                usbSendMSG(&msgSEND);
            }
        }
        else
        {
            if (msgSEND.type != 'E')
            {
                mvmtSTOP();
                msgSEND.type = 'E';
                msgSEND.state = 'S';
                msgSEND.frontDistance = irfront;
                msgSEND.id++;
                usbSendMSG(&msgSEND);
            }
        }

        break;

    case 'L':
        if (msgSEND.type != 'L')
        {
            msgSEND.type = 'L';
            msgSEND.state = 'T';
            msgSEND.id++;
            usbSendMSG(&msgSEND);
        }
        if (setSpdL == 0 && setSpdR == 0)
        {
            mvmtLEFTStatic(angleToTicks(90));
        }
        else
        {
            mvmtLEFT(angleToTicks(90));
        }
        if (msgSEND.type != 'F')
        {
            msgSEND.type = 'F';
            msgSEND.state = 'F';
            msgSEND.id++;
            usbSendMSG(&msgSEND);
        }
        break;

    case 'R':
        if (msgSEND.type != 'R')
        {
            msgSEND.type = 'R';
            msgSEND.state = 'T';
            msgSEND.id++;
            usbSendMSG(&msgSEND);
        }
        if (setSpdL == 0 && setSpdR == 0)
        {
            mvmtRIGHTStatic(angleToTicks(90));
        }
        else
        {
            mvmtRIGHT(angleToTicks(90));
        }
        if (msgSEND.type != 'F')
        {
            msgSEND.type = 'F';
            msgSEND.state = 'F';
            msgSEND.id++;
            usbSendMSG(&msgSEND);
        }
        break;

    case 'E':

    case 'S':
        mvmtSTOP();
        D_STREAM("Movement stopped");
        if (msgSEND.type != 'S')
        {
            msgSEND.type = 'S';
            msgSEND.state = 'S';
            msgSEND.id++;
            usbSendMSG(&msgSEND);
        }
        break;
    }
}

void stringCommands(char commands[], int len)
{
    static int calCounter = 0;
    static int x;

    switch (commands[x])
    {
    case 'f':
        if (setSpdL == 0 && setSpdR == 0)
        {
            setSpdL = MAXSPEED_L;
            setSpdR = MAXSPEED_R;
        }
        mvmtFORWARD();
        break;

    case 'l':
        if (setSpdL == 0 && setSpdR == 0)
        {
            mvmtLEFTStatic(angleToTicks(90));
        }
        else
        {
            mvmtLEFT(angleToTicks(90));
        }
        break;

    case 'r':
        if (setSpdL == 0 && setSpdR == 0)
        {
            mvmtRIGHTStatic(angleToTicks(90));
        }
        else
        {
            mvmtRIGHT(angleToTicks(90));
        }
        break;

    case 's':
        mvmtSTOP();
        break;

    case 'i':
        while (1)
        {
            scanFORWARD();
        }
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

