#include <DualVNH5019MotorShield.h>

DualVNH5019MotorShield md;

void setup()
{
    md.init();

    md.setSpeeds(400, 400);
    delay(2000);
    md.setBrakes(1, 1);
}

void loop()
{
}