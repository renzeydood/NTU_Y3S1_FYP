#define ARDUINO_UPDATE                             0x01
#define ARDUINO_INSTRUCTION                        0x02
#define ARDUINO_STREAM                             0x03

#define START									                     0x01
#define SCAN									                     0x02
#define TURN_LEFT                                  0x03
#define TURN_RIGHT                                 0x04
#define FORWARD                                    0x05
#define REVERSE									                   0x06
#define STOP                                       0x07
#define CAL_CORNER                                 0x08 
#define CAL_SIDE                                   0x09
#define TURN_ABOUT                                 0x10
#define CAL_ANY                                    0x11
#define CAL_FORWARD                                0x12
#define CAL_SIDE_FORWARD                           0x13
#define PAYLOAD_SIZE                               128 //As long as it's bigger than StatusMessage

struct Message
{
  uint8_t type; // To be checked by the Raspberry Pi
  uint8_t payload[8];
};

// 1 byte each
struct StatusMessage
{
  uint8_t id;
  uint8_t front1;
  uint8_t front2;
  uint8_t front3;
  uint8_t right1;
  uint8_t right2;
  uint8_t left1;
  uint8_t calibrated;
};

struct InstructionMessage
{
  uint8_t id;
  uint8_t action;
  uint8_t calibrateFirst;
};

struct StreamMessage
{
  uint8_t id;
  uint8_t calibrateFirst;
  uint8_t streamActions[PAYLOAD_SIZE]; //in case theres a lot of actions..
};


#define BUFFER_SIZE                               256



// timer
bool yetToReceiveAck = false;
bool alreadyReceived = false;
unsigned long timer = millis();
unsigned long timeout = 10000; // 250 milliseconds
