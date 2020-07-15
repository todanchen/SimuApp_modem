import time
import socket
from select import select
import random
import traceback


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('124.160.127.162', 6003))
    #server.bind(('127.0.0.1', 8001))
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
                        date_rate = int(flag[1])
                except:
                    traceback.print_exc()
                    break

                if not flag:
                    r.close()
                    print('data_link end, exit')
                    rlist.remove(r)

                elif 'request' in flag:
                    time_slic = random.randint(3, 23)
                    data = bytes(date_rate*time_slic)
                    B += time_slic
                    try:
                        r.send(data)
                        time.sleep(0.01)
                        signal = 'next' + ',' + str(time_slic) + ','
                        r.send(signal.encode())
                        print('next: ', B)
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
