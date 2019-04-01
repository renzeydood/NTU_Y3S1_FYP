#include <Streaming.h>
#include <SharpIR.h>
#include <DualVNH5019MotorShield.h>
#include "Settings.h"

void setup()
{
  Serial.begin(9600);
  Serial.println("Robot: Hello World!");
  md.init();

  attachInterrupt(digitalPinToInterrupt(11), encLeft, RISING);
  attachInterrupt(digitalPinToInterrupt(13), encRight, RISING);

  delay(2000);
  Serial.println("Initializations Done");
  delay(1000);
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
    //delay(1000);
  }
}

//------------Functions for robot movements------------//
void goFORWARD(int distance)
{
  long lastTime = micros();
  int setSpdR = 350; //400;                //Original: 300
  int setSpdL = 350; //400;                //Original: 300
  int colCounter = 0;
  resetMCounters();
  lastError = 0;
  totalErrors = 0;
  lastTicks[0] = 0;
  lastTicks[1] = 0;
  if (!(rfwdIrVal.distance() < 130 || lfwdIrVal.distance() < 130 || mfwdIrVal.distance() < 120))
  {
    int i = 50;
    md.setSpeeds(setSpdR, setSpdL);
    lastTime = millis();

    if (distance <= 1500)
    {
      while (mCounter[0] < distance && mCounter[1] < distance)
      {
        if (millis() - lastTime > 100)
        {
          if (checkFRONT())
          {
            break;
          }
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
      scanFORWARD(&irFrontReadings[0]);
      //    while ((mCounter[0] < distance - 445 && mCounter[1] < distance - 445) && ((irFrontReadings[0] > breakDist) || (irFrontReadings[1] > breakDist) || (irFrontReadings[2] > breakDist))){
      while (mCounter[0] < distance && mCounter[1] < distance)
      {
        if ((irFrontReadings[0] < (breakDist + 20)) || (irFrontReadings[1] < breakDist) || (irFrontReadings[2] < (breakDist + 20)))
        {
          //          mCounter[0] =  distance - 445;
          //          mCounter[1] =  distance - 445;                                 //Ends the forward movement and prevents the deleration in belows code
          break;
        }
        scanFORWARD(&irFrontReadings[0]);
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
  }
  delay(100);
}

void goRIGHT(int angle)
{
  int setSpdR = -300; //Right motor
  int setSpdL = 306;  //Left motor
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
  int setSpdR = 300;  //Right motor
  int setSpdL = -315; //Left motor
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

void calibrateRIGHT()
{
  scanRIGHT(&irRightReadings[0]);

  offsetOrientation = 0;
  offsetOrientation = irRightReadings[0] - irRightReadings[1];

  int turnTicks = 0;
  while (abs(irRightReadings[0] - irRightReadings[1]) > 4 && (abs(irRightReadings[0] - irRightReadings[1]) <= 70))
  {
    resetMCounters();

    turnTicks = (irRightReadings[0] - irRightReadings[1]) * 2;

    //Tick Reduction
    if ((abs(irRightReadings[0] - irRightReadings[1]) == 10) && abs(turnTicks) > 20)
    {
      turnTicks -= 1;
    }

    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-150, 150);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(150, -150);
      }
    }
    md.setBrakes(400, 400);
    delay(100);
    scanRIGHT(&irRightReadings[0]);
  }
}

void calibrateFRONT()
{
  scanFORWARD(&irFrontReadings[0]);
  int turnTicks = 0;
  while (abs(irFrontReadings[2] - 100) > 5 && abs(irFrontReadings[0] - 100) > 5)
  {
    resetMCounters();
    turnTicks = (irFrontReadings[0] - 100) * 2; // old multiplier is 20
    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(200, 200);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-200, -200);
      }
    }

    //Serial.println("irfrontreadings[0] V1");
    //Serial.println(irFrontReadings[0]);
    md.setBrakes(400, 400);
    delay(100);
    scanFORWARD(&irFrontReadings[0]);
  }
}

void calibrateCORNER()
{
  calibrateRIGHT();
  delay(100);
  calibrateFRONTV2();
  delay(100);
  goRIGHT(angleToTicks(90));
  delay(100);
  calibrateFRONT();
  delay(100);
  goLEFT(angleToTicks(90));
  delay(100);
  calibrateRIGHT();
}

void calibrateRIGHTV2()
{
  scanRIGHT(&irRightReadings[0]);
  int turnTicks = 0;
  //  Serial << "start" << endl ;
  while (abs(irRightReadings[0] % 100 - irRightReadings[1] % 100) > 5 && abs(irRightReadings[0] - irRightReadings[1]) < 200)
  {
    resetMCounters();
    int Fdist = irRightReadings[0];
    int Bdist = irRightReadings[1];
    if (Fdist / 100 == Bdist / 100)
    {
      if (Fdist < Bdist)
      {
        Bdist = Bdist + 99 - Fdist % 100;
        Fdist = Fdist + 99 - Fdist % 100;
      }
      else
      {
        Fdist = Fdist + 99 - Bdist % 100;
        Bdist = Bdist + 99 - Bdist % 100;
      }
    }
    else if (abs(Fdist / 100 - Bdist / 100) > 1)
    {
      int cnt = 10 + 100 * (abs(Fdist / 100 - Bdist / 100) - 1);
      if (Fdist % 100 > Bdist % 100)
      {
        Bdist = Bdist + (cnt - Fdist % 100);
        Fdist = Fdist + (cnt - Fdist % 100);
      }
      else
      {
        Fdist = Fdist + (cnt - Bdist % 100);
        Bdist = Bdist + (cnt - Bdist % 100);
      }
    }
    turnTicks = (Fdist % 100 - Bdist % 100) * 2;
    //Tick Reduction
    if (abs((Fdist - Bdist) % 100) == 1 && abs(turnTicks) > 20)
    {
      turnTicks -= 1;
    }

    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-150, 150);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(150, -150);
      }
    }
    md.setBrakes(400, 400);
    delay(100);
    scanRIGHT(&irRightReadings[0]);
  }
}

bool checkFRONT()
{
  int moveTicks = 0;
  if (rfwdIrVal.distance() < 110 || lfwdIrVal.distance() < 110 || mfwdIrVal.distance() < 100)
  {
    md.setBrakes(400, 400);
    return true;
  }
  return false;
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

//------------Experimental------------//
void calibrateFRONTV2()
{
  int zTicks = 0;
  scanFORWARD(&irFrontReadings[0]);
  int turnTicks = 0;
  while (abs(irFrontReadings[2] - 100) > 5 && abs(irFrontReadings[0] - 100) > 5)
  {
    resetMCounters();
    turnTicks = (irFrontReadings[0] - 100) * 2;
    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(200, 200);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-200, -200);
      }
    }
    md.setBrakes(400, 400);
    delay(100);
    scanFORWARD(&irFrontReadings[0]);
    //Serial.println("irfrontreadings[0] V2");
    //Serial.println(irFrontReadings[0]);
    zTicks += turnTicks;
  }
  if (mvmtCounter[0] != 0 && forwardOffsetCounter > 0)
  {
    ticksToMove = ticksToMove + ((kTicks * zTicks / mvmtCounter[0]) / 2);
  }
}

void calibrateFRONTV3()
{
  int zTicks = 0;
  int turnTicks = 0;
  // int target1 = 0;
  // int target2 = 0;
  int use = 0;
  scanFORWARD(&irFrontReadings[0]);
  if (abs(irFrontReadings[2] - 100) > 5 && irFrontReadings[2] < 150)
  {
    use = 2;
  }
  else if (abs(irFrontReadings[1] + 10 - 100) > 5 && irFrontReadings[1] + 10 < 150)
  {
    use = 1;
  }
  else if (abs(irFrontReadings[0] - 100) > 5 && irFrontReadings[0] < 150)
  {
    use = 0;
  }
  else
  {
    return;
  }
  do
  {
    scanFORWARD(&irFrontReadings[0]);
    resetMCounters();
    // if (abs(irFrontReadings[0] - 100) > 5 && abs(irFrontReadings[2] - 100) > 5 && irFrontReadings[0] < 150 &&  irFrontReadings[2] < 150) {
    //   target1 = irFrontReadings[0];
    //   target2 = irFrontReadings[2];
    // }
    // else if (abs(irFrontReadings[1] + 10 - 100) > 5 && abs(irFrontReadings[2] - 100) > 5 && irFrontReadings[1] + 10 < 150 &&  irFrontReadings[2] < 150) {
    //   target1 = irFrontReadings[1] + 10;
    //   target2 = irFrontReadings[2];
    // }
    // else if (abs(irFrontReadings[0] - 100) > 5 && abs(irFrontReadings[1]+ 10 - 100) > 5 && irFrontReadings[0] < 150 &&  irFrontReadings[1] + 10 < 150) {
    //   target1 = irFrontReadings[0];
    //   target2 = irFrontReadings[1] + 10;
    // }
    // if (abs(irFrontReadings[2] - 100) > 5 && irFrontReadings[2] < 150) {
    //   target1 = irFrontReadings[2];
    //   target2 = 106;
    // }
    // else if (abs(irFrontReadings[1] + 10 - 100) > 5 && irFrontReadings[1] + 10 < 150 ) {
    //   target1 = irFrontReadings[1] + 10;
    //   target2 = 106;
    // }
    // else if (abs(irFrontReadings[0] - 100) > 5 && irFrontReadings[0] < 150) {
    //   target1 = irFrontReadings[0];
    //   target2 = 106;
    // }
    // else {
    //   return;
    // }

    turnTicks = (irFrontReadings[use] - 100) * 2;
    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(200, 200);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-200, -200);
      }
    }
    md.setBrakes(400, 400);
    delay(100);
    zTicks += turnTicks;
  } while (abs(irFrontReadings[use] - 100) > 5);
  if (mvmtCounter[0] != 0 && forwardOffsetCounter > 0)
  {
    ticksToMove = ticksToMove + ((kTicks * zTicks / mvmtCounter[0]) / 2);
  }
}

void calibrationPhase1()
{

  calibrateCORNER();

  delay(200);
  int cycle = 4;

  for (int i = 0; i < cycle; i++)
  {
    goLEFT(angleToTicks(90));
    delay(200);
  }
  calibrateOffset(cycle, 0);
  delay(200);

  for (int i = 0; i < cycle; i++)
  {
    goRIGHT(angleToTicks(90));
    delay(200);
  }
  calibrateOffset(cycle, 1);
  delay(200);

  for (int i = 0; i < cycle; i++)
  {
    goLEFT(angleToTicks(180));
    delay(200);
  }
  calibrateOffset(cycle, 2);
  delay(200);
}

// flag = 0: LEFT offset, 1: RIGHT offset, 2: ABOUT_TURN offset, 3: FORWARD pull-pull back ticks
void calibrateOffset(int cycle, int flag)
{

  int frontRight = irRightReadings[0];
  int backRight = irRightReadings[1];

  int offset = 0;

  scanRIGHT(&irRightReadings[0]);
  int turnTicks = 0;
  while (abs(irRightReadings[0] - irRightReadings[1]) > 2 && (abs(irRightReadings[0] - irRightReadings[1]) <= 70))
  {
    resetMCounters();

    turnTicks = (irRightReadings[0] - irRightReadings[1]) * 2;

    //Tick Reduction
    if ((abs(irRightReadings[0] - irRightReadings[1]) == 10) && abs(turnTicks) > 20)
    {
      turnTicks -= 1;
    }

    offset += turnTicks;

    if (turnTicks > 0)
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(-150, 150);
      }
    }
    else
    {
      while (mCounter[0] < abs(turnTicks) && mCounter[1] < abs(turnTicks))
      {
        md.setSpeeds(150, -150);
      }
    }
    md.setBrakes(400, 400);
    delay(100);
    scanRIGHT(&irRightReadings[0]);
  }

  delay(200);

  switch (flag)
  {
  case 0:
    turnLeftTicks = turnLeftTicks + ((offset / cycle) / 2);
    break;
  case 1:
    turnRightTicks = turnRightTicks - ((offset / cycle) / 2);
    break;

  case 2:
    aboutTurnOffset = aboutTurnOffset + ((offset / cycle) / 2);
    break;
  }
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
  Serial << "FORWARD: <- Left: " << pData[0] << " () Mid: " << pData[1] << " -> Right: " << pData[2] << " \n"
         << endl;
}

void scanRIGHT(int *pData)
{
  pData[0] = frgtIrVal.distance(); //Right Front
  delay(2);
  pData[1] = brgtIrVal.distance(); //Right Back
  delay(2);
  Serial << "RIGHT: -> Right(Short): " << pData[0] << " -> Right(Long): " << pData[1] << " \n"
         << endl;
}

void scanLEFT()
{
  irLeftReading = flftIrVal.distance();
  delay(2);
  Serial << "LEFT: <- Left(Long): " << irLeftReading << " \n"
         << endl;
}

//------------Functions for Motors------------//
void resetMCounters()
{
  mCounter[0] = 0;
  mCounter[1] = 0;
}

//ISR for Motor 1 (Right) Encoders
void encLeft()
{
  mCounter[1]++;
}

void encRight()
{
  mCounter[0]++;
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
    fwdCorrection();
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

  case 4:
    Serial.println("Calibrate Right");
    scanRIGHT(&irRightReadings[0]);
    if (calCounter >= CalPeriod)
    {
      if (abs(irRightReadings[0] - irRightReadings[1]) > 5 && (abs(irRightReadings[0] - irRightReadings[1]) <= 70))
      {
        calibrateRIGHT();
        if ((irRightReadings[0] <= 90 || irRightReadings[0] >= 110))
        {
          delay(100);
          goRIGHT(angleToTicks(90));
          calibrateFRONT();
          delay(100);
          goLEFT(angleToTicks(90));
          calibrateRIGHT();
        }
        calCounter = 0;
      }
    }
    break;

  case 5:
    Serial.println("Doing Full Scan");
    scanFORWARD(&irFrontReadings[0]);
    scanLEFT();
    scanRIGHT(&irRightReadings[0]);
    Serial << "Left Forward IR: " << shortIrVal(irFrontReadings[0], 4, 340, lfwdIrOS) << " blocks away, actual: " << irFrontReadings[0] << endl;
    Serial << "Mid Forward IR: " << shortIrVal(irFrontReadings[1], 3, 350, mfwdIrOS) << " blocks away, actual: " << irFrontReadings[1] << endl;
    Serial << "Right Forward IR: " << shortIrVal(irFrontReadings[2], 3, 340, rfwdIrOS) << " blocks away, actual: " << irFrontReadings[2] << endl;
    Serial << "Front Right IR: " << shortIrVal(irRightReadings[0], 3, 360, frgtIrOS) << " blocks away, actual: " << irRightReadings[0] << endl;
    Serial << "Back Right IR: " << shortIrVal(irRightReadings[1], 3, 360, brgtIrOS) << " blocks away, actual: " << irRightReadings[1] << endl;
    Serial << "Left Long IR: " << longIrVal(irLeftReading, 5, 65, flftIrOS) << " blocks away, actual: " << irLeftReading << endl;
    break;

  case 6:
    Serial.println("Calibrate At Corner");
    calibrateCORNER();
    calCounter = 0;
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

  case 9:
    Serial.println("Calibrate At Any blocks");
    scanRIGHT(&irRightReadings[0]);
    if (abs(irRightReadings[0] - irRightReadings[1]) < 200 && abs(irRightReadings[0] - irRightReadings[1]) > 50)
    {
      Serial << "V2" << endl;
      calibrateRIGHTV2();
    }
    else
    {
      Serial << "Normal" << endl;
      calibrateRIGHT();
    }
    break;
  }
  delay(commandsDelay);

  if (x <= sizeof(commands) / sizeof(int))
  {
    x++;
  }
}

int shortIrVal(int val, int blockThreshold, int cmThreshold, int offset)
{

  int newVal = (val - offset) / 100;
  if (val < 100)
  {
    newVal = 1;
  }
  if (newVal > blockThreshold || val >= cmThreshold || val <= 0)
  {
    newVal = 0;
  }
  return newVal;
}

int longIrVal(int val, int blockThreshold, int cmThreshold, int offset)
{
  int newVal = (val - offset) / 10;
  if (val <= 17)
  {
    newVal = 1;
  }

  if (newVal >= blockThreshold || val >= cmThreshold)
  {
    newVal = 0;
  }
  return newVal;
}