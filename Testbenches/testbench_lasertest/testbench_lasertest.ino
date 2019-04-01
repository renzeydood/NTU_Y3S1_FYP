#include "Adafruit_VL53L0X.h"
#include "Streaming.h"

#define LASER_DELAY 100

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup()
{
    Serial.begin(115200);

    while (!Serial)
    {
        delay(1);
    }
    Serial.println("Adafruit VL53L0X test");
    laser_errorhandler();
}

void loop()
{
    Serial << "Laser reading: " << laser_getreading(lox) << endl;
}

void laser_errorhandler()
{
    if (!lox.begin())
    {
        Serial << "ERROR: Failed to boot VL53L0X ... Check your wiring!" << endl;
        while (1)
            ;
    }
    else
    {
        Serial << "VL53L0X setup successful" << endl;
    }
}

long laser_getreading(Adafruit_VL53L0X l_sensor)
{
    VL53L0X_RangingMeasurementData_t measure;
    l_sensor.rangingTest(&measure, false); // pass in 'true' to get debug data printout!
    long val = 0;

    if (measure.RangeStatus != 4)
    { // phase failures have incorrect data
        val = measure.RangeMilliMeter;
    }
    else
    {
        val = 0;
    }
    delay(LASER_DELAY);
    return val;
}