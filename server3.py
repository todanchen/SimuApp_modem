import time
import socket
from select import select
import sys


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('124.160.127.162', 8080))
#     server.bind(('127.0.0.1', 8001))
    server.listen(5)

    accept(server)


def accept(server):
    rlist = [server]
    wlist = []
    xlist = []
    types = 0
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
                    pass

                if not flag:
                    pass
                elif 'initial' in flag:
                    types = 1
                elif 'request' in flag:
                    types = 2
                elif 'stop' in flag:
                    types = 3
                    pause_start = time.time()
                    Bx = (B - 12)
                    sleeptime = Bx*8
                    B = B - Bx
                    print("Stop send the video data, this time: ", time.time(), '------value_B: ', B)
                elif 'Exit' in flag:
                    types = 0
                    r.close()
                    print('data_link end, exit')
                    rlist.remove(r)
                    
        if types == 1:
            date_rate = int(flag.split(',')[1])
            vdata = bytes(date_rate*8*5)
            mdata = vdata + 'start'.encode()
            B = 5
            r.send(mdata)
            print('Initial the video, this time: ', time.time(), '------value_B: ', B)
        elif types == 2:
            date_rate = int(flag.split(',')[1])
            vdata = bytes(date_rate * 8)
            mdata = vdata + 'end'.encode()
            B += 1
            r.send(mdata)
            print('Send the next video clice, this time: ', time.time(), '------value_B: ', B)
        elif types == 3:
            pause_time = time.time() - pause_start
            if pause_time >= sleeptime:
                r.send('exit'.encode())
                print('Pause end.')
            else:
                r.send('none'.encode())
                print('Pause')
        elif types == 0:
            pass

if __name__ == '__main__':
    main()
