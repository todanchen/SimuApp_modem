import time
import socket
from select import select
import sys


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind(('124.160.127.162', 8001))
    server.bind(('127.0.0.1', 8001))
    server.listen(5)

    accept(server)


def accept(server):
    rlist = [server]
    wlist = []
    xlist = []
    type = 0
    i = 0
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is server:
                conn, addr = server.accept()
                rlist.append(conn)
                print('Have a new Conn')
            else:
                try:
                    flag = r.recv(1024).decode()
                except:
                    r.close()
                    pass

                if not flag:
                    pass
                elif 'initial' in flag:
                    type = 1
                elif 'request' in flag:
                    type = 2
                elif 'stop' in flag:
                    type = 3
        if type == 1:
            date_rate = int(flag.split(',')[1])
            vdata = bytes(date_rate*8*5)
            mdata = vdata + 'start'.encode()
            B = 5
            r.send(mdata)
            print('Initial the video, this time: ', time.time(), '------value_B: ', B)
        elif type == 2:
            date_rate = int(flag.split(',')[1])
            vdata = bytes(date_rate * 8)
            mdata = vdata + 'end'.encode()
            B += 1
            r.send(mdata)
            print('Send the next video clice, this time: ', time.time(), '------value_B: ', B)
        elif type == 3:
            print("Stop send the video data, this time: ", time.time(), '------value_B: ', B)
            Bx = (B - 12)
            sleeptime = Bx*8
            B = B - Bx
            time.sleep(sleeptime)
            r.send('exit'.encode())
            print('Pause end.')

if __name__ == '__main__':
    main()