//---------------------Include necessary libraries.---------------------//
#include <Streaming.h>
//#include <SharpIR.h>
#include <DualVNH5019MotorShield.h>
#include <PID_v1.h>
#include "message_structure.h"

//---------------------Control print modes for debugging.---------------------//
#ifdef DEBUG
#define D if (1)
#else
#define D if (0) //Change this: 1 = Debug mode, 0 = Disable debug prints
#endif

//---------------------Pin Definitions. Instead of storing in int, saves RAM.---------------------//
#define m1EncA 3  //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
#define m1EncB 5  //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
#define m2EncA 13 //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
#define m2EncB 11 //Microcontroller pin 19, PORTB, PCINT0_vect, PCINT5

#define mfwdIrPin A0 //Middle forward IR

//---------------------Global Variables---------------------//
volatile int mCounter[2] = {0, 0}; //[0]right, [1]left, used for encoder tick values

//Variables for PID to work
double kp = 0.2;
double ki = 0;
double kd = 0;
double diffIn;
double diffOut;
double diffSP;

int setSpdL = 0;
int setSpdR = 0;

//---------------------Instantiate libraries when needed---------------------//
DualVNH5019MotorShield md; //NOTE: M1 = right motor, M2 = left motor
RCVDMessage msgRCVD;
SENDMessage msgSEND;

#define shrtmodel 1080
#define longmodel 20150
//SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0365, 0.060);
PID diffPID(&diffIn, &diffOut, &diffSP, kp, ki, kd, DIRECT);

//---------------------Communication related Variables.---------------------//
static int RPI_DELAY = 500;
static int ARD_DELAY = 0;
static char commands[] = {'f', 'f', 'f', 'f', 's', 0};