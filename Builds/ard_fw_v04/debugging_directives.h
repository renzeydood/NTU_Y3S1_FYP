#if DEBUG_MODE == true
#define D_BEGIN(x) Serial.begin(x)
#define D_PRINT(x) Serial.print(x)
#define D_PRINTLN(x) Serial.println(x)
#define D_STREAM(x) Serial << x << endl
#define D_DELAY(x) delay(x)
#else
#define D_BEGIN(x)
#define D_PRINT(x)
#define D_PRINTLN(x)
#define D_STREAM(x)
#define D_DELAY(x)
#endif