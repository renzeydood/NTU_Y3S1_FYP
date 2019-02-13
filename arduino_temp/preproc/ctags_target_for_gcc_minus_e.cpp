# 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino"
# 1 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino"
# 2 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino" 2
# 3 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino" 2
# 4 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino" 2

DualVNH5019MotorShield md;
RCVDMessage msgRCVD;
SENDMessage msgSEND;

int send_no = 20;

void setup()
{
    Serial.begin(9600);
    pinMode(13, 0x1);
    digitalWrite(13, 0x0);
    md.init();
    memset(&msgRCVD, 0, sizeof(RCVDMessage));
    memset(&msgSEND, 0, sizeof(SENDMessage));

    msgSEND.type = '1';
    msgSEND.id = '2';
    msgSEND.state = '7';
    msgSEND.frontDistance = 340;
    msgSEND.bearings = 90;
}

void loop()
{
    usbReceiveMSG(&msgRCVD);

    if (msgRCVD.distance == 50 && msgRCVD.motorspeed == 400 && msgRCVD.motorangle == 360)
    {
        digitalWrite(13, 0x1);
    }

    else if (msgRCVD.distance == 250 && msgRCVD.motorspeed == 100 && msgRCVD.motorangle == 180)
    {
        digitalWrite(13, 0x0);
    }

    if (send_no > 0)
    {
        usbSendMSG(&msgSEND);
        delay(1000);
        send_no--;
    }

    delay(5);

    MotorTest();
}

void usbReceiveMSG(RCVDMessage *MSG_Buffer)
{
    static uint8_t tempBuffer[MAX_BYTE_DATA];
    static uint8_t tempByte = 0;
    static int index = 0;
    static boolean recieving = false;

    if (Serial.available() > 0 && index < MAX_BYTE_DATA + 1) //Total index + STOP byte
    {
        tempByte = Serial.read();
        Serial.println(tempByte);

        if (recieving == true)
        {
            if (tempByte != STOP)
            {
                tempBuffer[index] = tempByte;
                index++;
            }

            else
            {
                recieving = false;
                index = 0;

                MSG_Buffer->type = tempBuffer[0];
                MSG_Buffer->id = tempBuffer[1];
                MSG_Buffer->distance = ((uint16_t)tempBuffer[2] << 8) | tempBuffer[3];
                MSG_Buffer->motorspeed = ((uint16_t)tempBuffer[4] << 8) | tempBuffer[5];
                MSG_Buffer->motorangle = ((uint16_t)tempBuffer[6] << 8) | tempBuffer[7];
            }
        }

        else if (tempByte == START)
        {
            recieving = true;
        }

        delay(5);
    }
}

void usbSendMSG(SENDMessage *MSG_Buffer)
{
    byte writebuff[] = {START, MSG_Buffer->type, MSG_Buffer->id, MSG_Buffer->state, ((uint8_t)((MSG_Buffer->frontDistance) >> 8)), ((uint8_t)((MSG_Buffer->frontDistance)&0xff)), ((uint8_t)((MSG_Buffer->bearings) >> 8)), ((uint8_t)((MSG_Buffer->bearings)&0xff)), STOP};

    /* Serial.write(START);

    Serial.println(MSG_Buffer->type);

    Serial.println(MSG_Buffer->id);

    Serial.println(MSG_Buffer->state);

    Serial.println(highByte(MSG_Buffer->frontDistance));

    Serial.println(lowByte(MSG_Buffer->frontDistance));

    Serial.println(highByte(MSG_Buffer->bearings));

    Serial.println(lowByte(MSG_Buffer->bearings));

    Serial.write(STOP); */
# 108 "c:\\Users\\Renzey\\Workspaces\\-NTU_FYP_Project_Files\\testbench_rpicomm\\testbench_rpicomm.ino"
    Serial.write(writebuff, 10);
    //Serial << START << MSG_Buffer->type << MSG_Buffer->id << MSG_Buffer->state << highByte(MSG_Buffer->frontDistance) << lowByte(MSG_Buffer->frontDistance) << highByte(MSG_Buffer->bearings) << lowByte(MSG_Buffer->bearings) << STOP;
    //Serial.write(START + MSG_Buffer->type + MSG_Buffer->id + MSG_Buffer->state + highByte(MSG_Buffer->frontDistance) + lowByte(MSG_Buffer->frontDistance) + highByte(MSG_Buffer->bearings) + lowByte(MSG_Buffer->bearings) + STOP);
    //Serial.flush();
}

void MotorTest()
{
    static int state = 0;
    static int i = 0;

    if (state == 0 && i <= 400)
    {
        md.setM1Speed(i);
        delay(2);
        i++;
        if (i == 400)
        {
            state = 1;
        }
    }

    if (state == 1 && i >= -400)
    {
        md.setM1Speed(i);
        delay(2);
        i--;
        if (i == -400)
        {
            state = 2;
        }
    }

    if (state == 2 && i <= 0)
    {
        md.setM1Speed(i);
        delay(2);
        i++;
        if (i == 0)
        {
            state = 0;
        }
    }
}
