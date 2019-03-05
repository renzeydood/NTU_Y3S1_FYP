#define lowByte(w) ((uint8_t)((w)&0x7f))
#define highByte(w) ((uint8_t)((w) >> 7))

const uint8_t START = '!';
const uint8_t STOP = '~';
const uint8_t MOTOR_CONTROL = '2';
const uint8_t STATE_IDLE = '5';
const uint8_t STATE_MOVING = '6';
const uint8_t STATE_STOPPED = '7';
const uint8_t MAX_BYTE_DATA = 8;

struct RCVDMessage
{
    uint8_t type;
    uint8_t id;
    int distance;
    int motorspeed;
    int motorangle;
};

struct SENDMessage
{
    uint8_t type;
    uint8_t id;
    uint8_t state;
    int frontDistance;
    int bearings;
};