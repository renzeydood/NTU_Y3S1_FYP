#include <SharpIR.h>
#include <Streaming.h>

#define shrtmodel 1080
#define longmodel 20150

#define mfwdIrPin A0 //Middle forward IR
#define lfwdIrPin A1 //Left forward IR
#define rfwdIrPin A2 //Right forward IR

SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0329, 0.080);
SharpIR lfwdIrVal(lfwdIrPin, shrtmodel, 0.0343, 0.090);
SharpIR rfwdIrVal(rfwdIrPin, shrtmodel, 0.0345, 0.090);

int left = 0;
int mid = 0;
int right = 0;
int sum = 0;

int count = 8;

void setup()
{
    Serial.begin(9600);

    delay(1000);

    Serial.println("Starting...");
}

void loop()
{
    //while (count != 0)
    //{
    Serial.println("Reading...");
    for (int x = 0; x < 50; x++)
    {
        scanFORWARD();
        sum = sum + mid;
        delay(200);
    }
    sum = sum / 50;
    Serial << "Reading Average: " << sum << "" << endl;
    Serial.println("Swap...");
    delay(3000);
    //count--;
    //}
}

void scanFORWARD()
{
    //left = lfwdIrVal.distance(); //Left
    left = 0;
    delay(2);
    mid = mfwdIrVal.distance(); // Middle
    //mid = analogRead(mfwdIrPin);
    delay(2);
    //right = rfwdIrVal.distance(); //Right
    right = 0;
    delay(2);
    //Serial << "FORWARD: <- Left: " << left << " () Mid: " << mid << " -> Right: " << right << " \n"
    //       << endl;
}