import threading
import time
import serial



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

def txFunc():
    ser = serial.Serial('/dev/serial0', timeout=2)
    while True:
        rawCmds = raw_input("Enter command to send: ")
        cmds = 'S' + ''.join(aggregate_instruction(rawCmds)) + ';'
        print "cmds: ", cmds
        ser.write(cmds)
        # for cmd in cmds:
        #     print "cmd", cmd
        #     ser.write(cmd)

def rxFunc():
    ser = serial.Serial('/dev/serial0', timeout=2)
    while True:
        if(ser.in_waiting != 0):

            pass
            # opcode = ser.read(1)
            # print "data: ", str(opcode)
            # if(opcode == '$'):
            #     # byte = self.readData()
            #     try:
            #         bytes = ser.read(8)
            #     except:
            #         ser.close()
            #         ser = serial.Serial('/dev/serial2', timeout=2)
            #
            #         byte = []
            #
            #     print "Data recieved: ", bytes





txThread = threading.Thread(target = txFunc)
rxThread = threading.Thread(target = rxFunc)

txThread.start()
rxThread.start()
