import socket

def Main():
    host = '127.0.0.1'
    port = 500

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()
    print('Connection from: ' + str(addr))

    while True:
        data = c.recv(1024).decode('utf-8') #RECIEVE 1024 BYTES AT A TIME FROM CLIENT
        if not data:
            break
        print('From connected user: ' + str(data))
        data = data.upper()
        print("Sending... " + data)
        c.send(data.encode('utf-8'))
    c.close()

if __name__ == '__main__':
    Main()