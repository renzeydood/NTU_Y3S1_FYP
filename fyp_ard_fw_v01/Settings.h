
//---------------------Pin Definitions. Instead of storing in int, saves RAM.---------------------//
#define m1EncA 3  //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
#define m1EncB 5  //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
#define m2EncA 13 //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
#define m2EncB 11 //Microcontroller pin 19, PORTB, PCINT0_vect, PCINT5

#define mfwdIrPin A0 //Middle forward IR
#define lfwdIrPin A1 //Left forward IR
#define rfwdIrPin A2 //Right forward IR
#define frgtIrPin A5 //Front right IR. The only long range IR.
#define flftIrPin A3 //Front left IR
#define brgtIrPin A4 //Back right IR

//---------------------Definitions for IR Sensor---------------------//
#define mfwdIrOS -50 //Middle forward IR prev:-50
#define lfwdIrOS -40 //Left forward IR prev:-40
#define rfwdIrOS -40 //Right forward IR prev:-40
#define frgtIrOS -40 //Front right IR
#define flftIrOS -5  //Front left IR.  The only long range IR.
#define brgtIrOS -40 //Back right IR

#define shrtmodel 1080
#define longmodel 20150

//---------------------Definitions for Motors---------------------//
// Voltage: 6.224, overextend during turns
#define forwardOffsetTicks 120
#define pullBackDelay 13

int turnLeftTicks = 10;
int turnRightTicks = -400;
int aboutTurnOffset = 17;
int pullBackTicks = 0;

#define breakDist 140

//---------------------Global Variables---------------------//
volatile int mCounter[2] = {0, 0}; //[0]right, [1]left

int irFrontReadings[3] = {0, 0, 0}; //[0]left, [1]middle, [2]right
int irRightReadings[2] = {0, 0};    //[0]front, [1]back
int irLeftReading = 0;

int CalPeriod = 0;
int CrashChkPeriod = 5;

int offsetOrientation = 0;

int kTicks = 1; //Forward movement Constant multiplier
int ticksToMove = 1192;
//int zTicks = 0;                  //Forward movement ticks Error
int forwardOffsetCounter = 0;

uint8_t last_sent = 0; //Variable for communication

//Variables for PID to work
int lastTicks[2] = {0, 0};
int lastError;
int totalErrors;

int RPIExpDelay = 50; //This original is 20
int RPIFPDelay = 200;

int mvmtCounter[] = {0, 0, 0}; //[0]forward, [1]left, [2]right

//---------------------Functional Check---------------------//
int commandsDelay = 50;
int commands[] =
    //{0};                            //Set to commWithRPI mode
    //{1, 1, 1, 1, 3, 3, 1, 1};
    {2, 2, 2, 2};
//----------Step 1: Check sensors accuracy (5 mins)
//                {5};                          //IR Sensors, full scan

//----------Step 2: Check basic movements (10 mins)
//                {1,1,1,1,1,1,1,1,7,8,8,5};                //Forward movement, block by block
//{2,2,2,2,2,2,2,2,1,1,1};      //Left turns
//{3,3,3,3,3,3,3,3,1,1,1};      //Right turns
//{7,7,1,1,1};                  //Left turn 180
//                {4,8,15,0};                        //Forward burst movement (After the command, 8, the next number is the number of blocks)

//----------Step 3: Check calibrations (10 mins)
//                {4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1};                    //Calibrate side
//{6,7,1,1,1};                  //Calibrate corner
//                {1,9,1,1,9,1,1};                    //Calibrate with any blocks

//----------Step X: Specific movement patterns
//{3,1,3,1,3,1,3,1,1,1,1};      //Loop movement (When algorithm gets stuck)
//{1,1,1,1,1,1,3,1,3,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,3,1,3,1,1,1,1,1,1}; //Snake movement
//{1,3,1,2,1,3,1,2,1,3,1,2,1,3,1,2}; //Stairs

//{7,8,7,3,8,4,2,8,9,3,8,8,2,1};

//---------------------Instantiate IR and Motor objects from library---------------------//
//Voltage 6.26
SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0365, 0.060);
SharpIR lfwdIrVal(lfwdIrPin, shrtmodel, 0.0343, 0.090);
SharpIR rfwdIrVal(rfwdIrPin, shrtmodel, 0.0345, 0.090);
//SharpIR frgtIrVal(frgtIrPin, shrtmodel, 0.0366, 0.068);
SharpIR frgtIrVal(frgtIrPin, shrtmodel, 0.0370, 0.068);
SharpIR flftIrVal(flftIrPin, longmodel, 0.0150, 0.165);
//SharpIR flftIrVal(flftIrPin, longmodel, 0.0150, 0.245);
SharpIR brgtIrVal(brgtIrPin, shrtmodel, 0.0345, 0.081);

//Battery 1 (Strong Battery, max charge)
//SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0365, 0.060);
//SharpIR lfwdIrVal(lfwdIrPin, shrtmodel, 0.0343, 0.090);
//SharpIR rfwdIrVal(rfwdIrPin, shrtmodel, 0.0350, 0.080);
//SharpIR frgtIrVal(frgtIrPin, shrtmodel, 0.0363, 0.070);
//SharpIR flftIrVal(flftIrPin, longmodel, 0.0150, 0.165);
//SharpIR brgtIrVal(brgtIrPin, shrtmodel, 0.0360, 0.070);

//SharpIR mfwdIrVal(mfwdIrPin, shrtmodel, 0.0360, 0.060);
//SharpIR lfwdIrVal(lfwdIrPin, shrtmodel, 0.0340, 0.090);
//SharpIR rfwdIrVal(rfwdIrPin, shrtmodel, 0.0353, 0.080);
//SharpIR frgtIrVal(frgtIrPin, shrtmodel, 0.0363, 0.086);
//SharpIR flftIrVal(flftIrPin, longmodel, 0.01265, 0.16454);
//SharpIR brgtIrVal(brgtIrPin, shrtmodel, 0.03651, 0.065);

DualVNH5019MotorShield md;
//CustomMotorLib md;
RingBuffer usbBufferIn;
