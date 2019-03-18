//---------------------Include necessary libraries.---------------------//
#include <Streaming.h>
#include <SharpIR.h>
#include <DualVNH5019MotorShield.h>
#include "message_structure.h"

//---------------------Control print modes for debugging.---------------------//
#define DEBUG_MODE false
#include "debugging_directives.h"

//---------------------Pin Definitions. Instead of storing in int, saves RAM.---------------------//
#define m1EncA 3  //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
#define m1EncB 5  //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
#define m2EncA 13 //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
#define m2EncB 11 //Microcontroller pin 19, PORTB, PCINT0_vect, PCINT5

#define mfwdIrPin A0 //Middle forward IR

//---------------------Instantiate libraries when needed---------------------//
DualVNH5019MotorShield md; //NOTE: M1 = right motor, M2 = left motor
RCVDMessage msgRCVD;
SENDMessage msgSEND;

#define shrtmodel 1080
#define longmodel 20150
SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0365, 0.060);

//---------------------Global Variables---------------------//
volatile int mCounter[2] = {0, 0}; //[0]right, [1]left, used for encoder tick values

static int MAXSPEED_L = 230; //best speed, 280
static int MAXSPEED_R = 238; //best speed, 288

//Variables for PID to work
int lastTicks[2] = {0, 0};
int lastError;
int totalErrors;

int setSpdR = 0; //400;                //Original: 300
int setSpdL = 0; //400;                //Original: 300

int turnOffset = -150; //280,75
int turnOffsetStatic = 0;

//---------------------Communication related Variables.---------------------//
static int RPI_DELAY = 80;
static int ARD_DELAY = 80;
static char commands[] =
    {'0'};
//{'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 'f', 'f', 'f', 'f', 'f', 'f', 'l', 'f', 'f', 'f', 'f', 'f', 'f', 'r', 's'};
//{'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 'f', 's'};
//{'r', 's', 'r', 's'};
//{'f', 'f', 'r', 'f', 'f', 'r', 'f', 'f', 'l', 's', 's' 'r', 'r', 0};