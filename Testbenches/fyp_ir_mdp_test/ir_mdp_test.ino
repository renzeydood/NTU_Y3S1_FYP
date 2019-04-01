#include "SharpIR.h" //Note that the SharpIR library already does it's median filtering
#include "Streaming.h"

#define SHORT_IR 1080
#define LONG_IR 20150

#define PS1 A0
#define PS2 A1
#define PS3 A2
#define PS4 A3
#define PS5 A4
#define PS6 A5

const int SAMPLE = 50;
SharpIR ir(A0, SHORT_IR, 0.0329, 0.080);

void setup()
{
    Serial.begin(9600);

    delay(1000);

    Serial << "*******************************************************" << endl;
    Serial << "                   IR Sensor Testbench                 " << endl;
    Serial << "  Test if the IR Sensor is working and for precision   " << endl;
    Serial << "                 *Connect sensor to PS1                " << endl;
    Serial << "*******************************************************" << endl;
    Serial << " " << endl;
    delay(2000);

    Serial.print("IR model type (0=short, 1=long): ");
    while (!Serial.available())
        ;
    if (Serial.read() != 0)
    {
        Serial << "Model: Long IR" << endl;
        ir.setModel(SHORT_IR);
        ir.setIncpt(0.080);
        ir.setGrad(0.0329);
    }

    else
    {
        Serial << "Model: Short IR" << endl;
        ir.setModel(LONG_IR);
        ir.setIncpt(0.050);
        ir.setGrad(0.015);
    }

    Serial << "Starting..." << endl;
    Serial << " " << endl;
}

void loop()
{
    Serial.println("Reading...");
    Serial << "===> Reading Average: " << avgReading() << "cm" << endl;
    delay(3000);
}

int avgReading()
{
    int sum = 0;
    for (int x = 0; x < 50; x++)
    {
        sum = sum + ir.distance();
        delay(100);
    }
    sum = sum / 50;

    return sum;
}