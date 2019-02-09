#include <Streaming.h>
#include "message_structure.h"
#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;
RCVDMessage msgRCVD;
SENDMessage msgSEND;

void setup()
{
    Serial.begin(9600);
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    //md.init();
    memset(&msgRCVD, 0, sizeof(RCVDMessage));
    memset(&msgSEND, 0, sizeof(SENDMessage));

    msgSEND.type = '1';
    msgSEND.id = '2';
    msgSEND.state = '7';
    msgSEND.frontDistance = 340;
    msgSEND.bearings = 90;
}

void loop()
{
    /*     usbReceiveMSG(&msgRCVD);

    if (msgRCVD.distance == 200 && msgRCVD.motorspeed == 400 && msgRCVD.motorangle == 360)
    {
        digitalWrite(13, HIGH);
    }

    else if (msgRCVD.distance == 250 && msgRCVD.motorspeed == 100 && msgRCVD.motorangle == 180)
    {
        digitalWrite(13, LOW);
    } */

    usbSendMSG(&msgSEND);
    delay(1000);
}

void usbReceiveMSG(RCVDMessage *MSG_Buffer)
{
    static uint8_t tempBuffer[MAX_BYTE_DATA];
    static uint8_t tempByte = 0;
    static int index = 0;
    static boolean recieving = false;

    if (Serial.available() > 0 && index < MAX_BYTE_DATA + 1) //Total index + STOP byte
    {
        tempByte = Serial.read();
        Serial.println(tempByte);

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
                MSG_Buffer->distance = ((uint16_t)tempBuffer[2] << 8) | tempBuffer[3];
                MSG_Buffer->motorspeed = ((uint16_t)tempBuffer[4] << 8) | tempBuffer[5];
                MSG_Buffer->motorangle = ((uint16_t)tempBuffer[6] << 8) | tempBuffer[7];
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
    Serial.write(START);
    Serial.write(MSG_Buffer->type);
    Serial.write(MSG_Buffer->id);
    Serial.write(MSG_Buffer->state);
    Serial.write(highByte(MSG_Buffer->frontDistance));
    Serial.write(lowByte(MSG_Buffer->frontDistance));
    Serial.write(highByte(MSG_Buffer->bearings));
    Serial.write(lowByte(MSG_Buffer->bearings));
    Serial.write(STOP);
    Serial.flush();
}

void MotorTest()
{
    for (int i = 0; i <= 400; i++)
    {
        md.setM1Speed(i);
        delay(2);
    }

    for (int i = 400; i >= -400; i--)
    {
        md.setM1Speed(i);
        delay(2);
    }

    for (int i = -400; i <= 0; i++)
    {
        md.setM1Speed(i);
        delay(2);
    }

    for (int i = 0; i <= 400; i++)
    {
        md.setM2Speed(i);
        delay(2);
    }

    for (int i = 400; i >= -400; i--)
    {
        md.setM2Speed(i);
        delay(2);
    }

    for (int i = -400; i <= 0; i++)
    {
        md.setM2Speed(i);
        delay(2);
    }
}