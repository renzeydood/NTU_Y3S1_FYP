#396, split to 2 8 bytes = 0x01, 0x8C, 1 and 140
#     split to 2 7 bits  = 0x03, 0x0C, 3 and 12
#int to char = chr(i)
#char to int = ord(c)

START = '!'
STOP = '~'

upper = 0
lower = 0

upper = 396>>7
lower = 396&0x7F

revert = upper<<7 | lower

def int_to_bytes(data):
    return chr(data>>7) + chr(data&0x7F)

def bytes_to_int(u, l):
    return int(u<<7 | l)

d = ['A', 1, 50, 400, 360]
msg = (START + d[0] + chr(d[1]) + int_to_bytes(d[2]) + int_to_bytes(d[3]) + int_to_bytes(d[4]) + STOP).encode('ascii')

print(msg)
print(bytes_to_int(msg[3], msg[4]))
print(type(msg[3]))
#print(bytes_to_int(int_to_bytes(d[2])))