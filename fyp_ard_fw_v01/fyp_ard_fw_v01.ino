#include <Streaming.h>
#include <SharpIR.h>
#include <DualVNH5019MotorShield.h>
#include "communication.h"
#include "RingBuffer.h"
#include "Settings.h"

#ifdef DEBUG
#define D if (1)
#else
#define D if (0) //Change this: 1 = Debug mode, 0 = Disable debug prints
#endif

void setup()
{
    Serial.begin(115200);
    RingBuffer_init(&usbBufferIn);
    D Serial.println("Robot: Hello World!");
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

    delay(2000);
    D Serial.println("Initializations Done");
}

void loop()
{
    if (commands[0] != 0)
    {
        stringCommands();
        delay(1000);
    }
    else
    {
        //commWithRPI();
    }
}

//------------Functions for robot movements------------//
void goFORWARD(int distance)
{
    long lastTime = micros();
    int setSpdR = 380; //400;                //Original: 300
    int setSpdL = 400; //400;                //Original: 300
    int colCounter = 0;
    resetMCounters();
    lastError = 0;
    totalErrors = 0;
    lastTicks[0] = 0;
    lastTicks[1] = 0;
    //if (!(rfwdIrVal.distance() < 130 || lfwdIrVal.distance() < 130 || mfwdIrVal.distance() < 120))
    //{
    int i = 50;
    md.setSpeeds(setSpdR, setSpdL);
    lastTime = millis();

    if (distance <= 1500)
    {
        while (mCounter[0] < distance && mCounter[1] < distance)
        {
            if (millis() - lastTime > 100)
            {
                //if (checkFRONT())
                //{
                //    break;
                //}
                PIDControl(&setSpdR, &setSpdL, 40, 0, 40, 0); //By block 40, 0, 80, 0
                lastTime = millis();
                setSpdR = setSpdR - 1;
                setSpdL = setSpdL + 1;
                md.setSpeeds(setSpdR, setSpdL);
            }
        }
    }
    else
    {
        //scanFORWARD(&irFrontReadings[0]);
        //    while ((mCounter[0] < distance - 445 && mCounter[1] < distance - 445) && ((irFrontReadings[0] > breakDist) || (irFrontReadings[1] > breakDist) || (irFrontReadings[2] > breakDist))){
        while (mCounter[0] < distance && mCounter[1] < distance)
        {
            if ((irFrontReadings[0] < (breakDist + 20)) || (irFrontReadings[1] < breakDist) || (irFrontReadings[2] < (breakDist + 20)))
            {
                //          mCounter[0] =  distance - 445;
                //          mCounter[1] =  distance - 445;                                 //Ends the forward movement and prevents the deleration in belows code
                break;
            }
            //scanFORWARD(&irFrontReadings[0]);
            if (millis() - lastTime > 100)
            {
                PIDControl(&setSpdR, &setSpdL, 20, 0, 40, 0); //Current for 6.20-6.22 Long distance 30, 5, 60 prev
                lastTime = millis();
                setSpdR = setSpdR - 1;
                setSpdL = setSpdL + 1;
                md.setSpeeds(setSpdR, setSpdL);
            }
        }
    }
    md.setBrakes(400, 400);
    resetMCounters();
    //}
    delay(100);
}

void goRIGHT(int angle)
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
    while (mCounter[0] < angle - turnRightTicks - 200 && mCounter[1] < angle - turnRightTicks - 200)
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
    while (mCounter[0] < angle - turnRightTicks && mCounter[1] < angle - turnRightTicks)
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

void goLEFT(int angle)
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

    while (mCounter[0] < angle - turnLeftTicks - 200 && mCounter[1] < angle - turnLeftTicks - 200)
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
    while (mCounter[0] < angle - turnLeftTicks && mCounter[1] < angle - turnLeftTicks)
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
    totalErrors = 0;
    //   totalErrors += error             ;                                           //Add up total number of errors (for Ki)
    //  if (error != 0) {                                                           //if error exists
    adjustment = ((kP * error) - (kI * totalErrors) + (kD * errorRate)) / 100;
    //     adjustment = ((kP * error) + (kI * totalErrors) + (kD * errorRate)) / 100;
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
    // }
    //  Serial << "Adjustment: " << adjustment << endl;
    //  Serial << "error: " << error << " total error: " << totalErrors << " errorRate: " << errorRate << endl ;
}

void fwdCorrection()
{
    static int fwdCounter = 0;
    //int pullDist = ((mCounter[0] - mCounter[1])*1)/1 + (offsetOrientation*2);
    int pullDist = ((mCounter[0] - mCounter[1]) * 1) / 1;
    resetMCounters();

    scanRIGHT(&irRightReadings[0]);

    if (fwdCounter == 3)
    {
        if (pullDist > 0)
        {
            while (mCounter[0] < abs(pullDist))
            { //Right motor pull back
                md.setM1Speed(-350);
            }
        }

        //if(pullDist < 0){
        //while(mCounter[1] < abs(pullDist)){         //Left motor pull back
        //md.setM2Speed(-350);
        //}
        //}

        fwdCounter = 0;
    }
    fwdCounter++;

    md.setBrakes(400, 400);
}

int angleToTicks(long angle)
{
    if (angle == 90)
        return 16800 * angle / 1000;
    else
        return (17280 * angle / 1000) - aboutTurnOffset;
}

int blockToTicks(int blocks)
{
    if (blocks == 1)
        if (forwardOffsetCounter > 0)
            return (ticksToMove - forwardOffsetTicks) * blocks;
        else
            return 1200 * blocks;
    else
        return 1192 * blocks; //1192 * blocks;
}

//------------Functions for IR Sensors------------//
void scanFORWARD(int *pData)
{
    pData[0] = lfwdIrVal.distance(); //Left
    delay(2);
    pData[1] = mfwdIrVal.distance(); // Middle
    delay(2);
    pData[2] = rfwdIrVal.distance(); //Right
    delay(2);
    D Serial << "FORWARD: <- Left: " << pData[0] << " () Mid: " << pData[1] << " -> Right: " << pData[2] << " \n"
             << endl;
}

void scanRIGHT(int *pData)
{
    pData[0] = frgtIrVal.distance(); //Right Front
    delay(2);
    pData[1] = brgtIrVal.distance(); //Right Back
    delay(2);
    D Serial << "RIGHT: -> Right(Short): " << pData[0] << " -> Right(Long): " << pData[1] << " \n"
             << endl;
}

void scanLEFT()
{
    irLeftReading = flftIrVal.distance();
    delay(2);
    D Serial << "LEFT: <- Left(Long): " << irLeftReading << " \n"
             << endl;
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

void stringCommands()
{
    static int calCounter = 0;
    static int x;
    switch (commands[x])
    {
    case 1:
        Serial.println("Moving forward");
        goFORWARD(blockToTicks(1));
        mvmtCounter[0]++;
        calCounter++;
        break;

    case 2:
        Serial.println("Moving left");
        goLEFT(angleToTicks(90));
        calCounter++;
        break;

    case 3:
        Serial.println("Moving right");
        goRIGHT(angleToTicks(90));
        calCounter++;
        break;

    case 5:
        Serial.println("Doing Full Scan");
        scanFORWARD(&irFrontReadings[0]);
        scanLEFT();
        scanRIGHT(&irRightReadings[0]);
        break;

    case 7:
        Serial.println("About Turn");
        goLEFT(angleToTicks(180));
        calCounter++;
        break;

    case 8:
        Serial.println("Forward burst");
        goFORWARD(blockToTicks(commands[++x]));
        calCounter++;
        break;
    }
    delay(commandsDelay);

    if (x <= sizeof(commands) / sizeof(int))
    {
        x++;
    }
}
