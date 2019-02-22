from Vehicle import Vehicle

robot = Vehicle(shape = 1, qr = 1)


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

def rxFunction(data):
    #Run when input buffer is not empty
    #print data
    pass

def txFunction(dir):

    if dir == "Arrow facing right":
        robot.serialM.sendData("SD1;")
    elif dir == "Arrow facing left":
        robot.serialM.sendData("SA1;")

robot.startSerial(rxFunction, txFunction)
robot.startCamera()

while True:
    rawCmds = raw_input("Enter command to send: ")
    cmds = 'S' + ''.join(aggregate_instruction(rawCmds)) + ';'
    robot.serialM.sendData(cmds)
