#include <DynamixelWorkbench.h>

#define DXL_BUS_SERIAL1 "1"            //Dynamixel on Serial1(USART1)  <-OpenCM9.04
#define DXL_BUS_SERIAL2 "2"            //Dynamixel on Serial2(USART2)  <-LN101,BT210
#define DXL_BUS_SERIAL3 "3"            //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#define DXL_BUS_SERIAL4 "/dev/ttyUSB0" //Dynamixel on Serial3(USART3)  <-OpenCR

#define BAUDRATE 1000000
#define DXL_ID 1

DynamixelWorkbench dxl_wb;

void setup()
{
    //Serial.begin(115200);

    dxl_wb.begin(DXL_BUS_SERIAL4, BAUDRATE);
    dxl_wb.ping(DXL_ID);

    dxl_wb.wheelMode(DXL_ID);

    dxl_wb.begin(DXL_BUS_SERIAL4, BAUDRATE);
    dxl_wb.ping(2);

    dxl_wb.wheelMode(2);

    delay(1500);
}

void loop()
{
    dxl_wb.goalSpeed(DXL_ID, 200);
    dxl_wb.goalSpeed(2, 200);
    delay(1000);

    dxl_wb.goalSpeed(DXL_ID, -200);
    dxl_wb.goalSpeed(2, -200);
    delay(1000);
}