import time
import socket
from select import select
import sys


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('124.160.127.162', 8000))
    #server.bind(('127.0.0.1', 8001))
    server.listen(1)

    accept(server)


def accept(server):
    conn, addr = server.accept()
    print('Have a new Conn')
    Bi = 0
    rlist = [conn]
    wlist = []
    xlist = []
    while True:
        rs, ws, xs = select(rlist, wlist, xlist, 1)
        for r in rs:
            try:
                flag = conn.recv(1024).decode()
                date_rate = int(flag.split(',')[1])
                Bj = int(flag.split(',')[2])
            except:
                pass
            print(flag)
            if not flag:
                pass
            elif 'initial' in flag:
                v_data = bytes(date_rate*30)
                s_data = v_data + 'start'.encode()
                try:
                    conn.send(s_data)
                    Bi = 5
                    print('Initial the video, this time: ', time.time(), '------value_B: ', Bi)
                except:
                    pass
            elif 'request' in flag:
                if Bj >= 15:
                    sleeptime = 6*(Bi-15)
                    Bi = 15
                    print('need to sleep: ', sleeptime)
                    time.sleep(sleeptime)
                v_data = bytes(date_rate * 6)
                s_data = v_data + 'end'.encode()
                try:
                    conn.send(s_data)
                    Bi += 1
                    print('Send the next video clice, this time: ', time.time(), '------value_B: ', Bi)
                except:
                    pass
            elif 'Exit' in flag:
                conn.close()
                break





if __name__ == '__main__':
    main()
