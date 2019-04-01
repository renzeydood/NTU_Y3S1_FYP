#include "settings.h"

void setup()
{
    Serial.begin(9600);
    //D Serial.println("Robot: Hello World!");
    md.init();
    diffPID.SetMode(AUTOMATIC);

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
    resetMCounters();

    md.setSpeeds(setSpdR, setSpdL);
    //lastTime = millis();

    while (mCounter[0] < distance && mCounter[1] < distance)
    {
        //if (millis() - lastTime > 100)
        //{
        PIDControl(0, 0, 40); //By block 40, 0, 80, 0
        if (diffIn > 0)
        { //Right motor slow down
            setSpdL = (int)(setSpdL + diffOut / 2);
            setSpdR = (int)(setSpdR - diffOut / 2);
        }
        else
        { //Left motor slow down
            setSpdL = (int)(setSpdL - diffOut / 2);
            setSpdR = (int)(setSpdR + diffOut / 2);
        }

        //lastTime = millis();
        //Serial << "Input: " << diffIn << " Output: " << diffOut << endl;
        //Serial << "Right:" << setSpdR << " Left: " << setSpdL << endl;
        Serial.println((int)diffOut);
        md.setSpeeds(setSpdR, setSpdL);
        //}
    }

    //mvmtSTOP();
    //delay(100);
}

void mvmtRIGHT(int angle)
{
    int setSpdR = -400; //Right motor
    int setSpdL = 400;  //Left motor
    long lastTime = millis();
    resetMCounters();

    md.setSpeeds(setSpdR, setSpdL);
    delay(50);
    while (mCounter[0] < angle - 200 && mCounter[1] < angle - 200)
    {
        if (millis() - lastTime > 100)
        {
            //PIDControl(&setSpdR, &setSpdL, 150, 6, 15, 1);
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
    resetMCounters();

    md.setSpeeds(setSpdR, setSpdL);
    delay(50);

    while (mCounter[0] < angle - 200 && mCounter[1] < angle - 200)
    {
        if (millis() - lastTime > 100)
        {
            //PIDControl(&setSpdR, &setSpdL, 150, 6, 15, -1);
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

void PIDControl(double kP, double kI, double kD)
{
    //mCounter[0] = right, mCounter[1] = left,
    //If PID result is positive, decrease right,
    //If PID result is negative, decrease left
    diffIn = mCounter[0] - mCounter[1];
    diffSP = 0;

    if (abs(diffIn) > 10)
    {
        diffPID.Compute();
    }

    //No value to return, since output is global
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

    switch (commands[x])
    {
    case 'f':
        if (setSpdL == 0 && setSpdR == 0)
        {
            setSpdL = 350;
            setSpdR = 350;
        }
        mvmtFORWARD(blockToTicks(5));
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
