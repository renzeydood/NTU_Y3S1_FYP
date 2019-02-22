from Vehicle import Vehicle

#Application specific script (Main thread). Sample usage of the various classes.
#====================================================================================

#=======================App specific helper function=================================

def aggregate_instruction(instruction):
    if len(instruction) == 0:
        return []

    instruction_list = [ch + '1' for ch in instruction]
    updatedInstruction = [instruction_list[0]]
    for ch in instruction_list[1:]:
        if (ch[0] != updatedInstruction[-1][0]):
            updatedInstruction.append(ch)
        else:
            updatedInstruction[-1] = updatedInstruction[-1][0] + chr(ord(updatedInstruction[-1][1:]) + 1)
    return updatedInstruction

#=======================App specific Serial RX data handler============================

def rxFunction(data):
    #Run when input buffer is not empty
    #print data
    pass

#=======================App specific camera frame procssing instructions================

def cameraApp():

    #Find shapes/arrow
    shapesFound = robot.cam.findShapes()
    for shape in shapesFound :
        robot.cam.drawShapes(shape)
        # if shape.type == "Arrow":
        #     if shape.orientation == "Left":
        #         robot.serialM.sendData("SA1;")
        #     elif shape.orientation == "Right":
        #         robot.serialM.sendData("SD1;")

    #Find QRCode
    qrList = robot.cam.decodeQR()
    for qr in qrList:
        print "Data : ", qr.data, "\n"
    robot.cam.drawQR(qrList)

    #Display processed current video frame
    robot.cam.displayFrame()



#=======================Init the vehicle to start the app================
robot = Vehicle()
robot.startSerial(rxFunction)
robot.startCamera(cameraApp)

while True:
    rawCmds = raw_input("Enter command to send: ")
    cmds = 'S' + ''.join(aggregate_instruction(rawCmds)) + ';'
    robot.serialM.sendData(cmds)
