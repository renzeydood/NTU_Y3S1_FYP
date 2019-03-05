import serial

ser = serial.Serial('9', '9600')

ser.write('1')

while(1):
    if(ser.inWaiting() > 0):
        tempBytes = ser.read()
        print(tempBytes)
