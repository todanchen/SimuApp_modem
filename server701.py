import time
import socket
from select import select
import random
import traceback


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
                    if flag:
                        flag = flag.split(',')
                        date_rate = flag[1]
                except:
                    traceback.print_exc()
                    pass

                if not flag:
                    pass
                elif 'initial' in flag:
                    data = bytes(date_rate*25)
                    B = 25
                    try:
                        r.send(data)
                        time.sleep(0.15)
                        signal = 'start'+',' + str(B) + ','
                        r.send(signal.encode())
                    except:
                        traceback.print_exc()
                        pass
                elif 'request' in flag:
                    time_slic = random.randint(3, 23)
                    data = bytes(date_rate*time_slic)
                    B += data
                    try:
                        r.send(data)
                        time.sleep(0.15)
                        signal = 'next' + ',' + str(B) + ','
                        r.send(signal.encode())
                    except:
                        traceback.print_exc()
                        pass
                elif 'Exit' in flag:
                    r.close()
                    print('data_link end, exit')
                    rlist.remove(r)

        time.sleep(0.05)




if __name__ == '__main__':
    main()
