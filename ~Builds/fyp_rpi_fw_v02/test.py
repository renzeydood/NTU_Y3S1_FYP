from message_structure import *
from test2 import *

class Test():
    def __init__(self):
        self.a = AnotherTest()
        self.msg = RCVDMessage()

    def send(self):
        print(id(self.msg))
        self.msg.id = 2
        self.a.rcvd(self.msg)

    def msgself(self):
        self.d = self.msg.toInt()
        print(self.d.id)


t = Test()

r = b'\x00'.decode()

c = chr(0)

somestr = "heyyy"

print(type(c))




    