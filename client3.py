import time
import socket
from select import select
import sys

def main(date_rate):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(('139.196.8.20', 8080))
    client.setblocking(False)
    # client.connect(('127.0.0.1', 8001))
    print('连接至服务器')
    connect(client, date_rate)


def connect(client, date_rate):
    rlist = [client]
    wlist = []
    xlist = []
    connectime = time.time()
    B = 0

    length = 1
    ratetime = connectime

    initial_falg = 'initial' + ',' + str(date_rate)
    request_falg = 'request' + ',' + str(date_rate)
    stop_falg = 'stop'+ ',' + str(date_rate)
    client.send(initial_falg.encode())
    print('发送数据')
    while True:
        time.sleep(0.01)
        # endtime = time.time() - connectime
        # if endtime > 600:
        #     client.close()
        #     time.sleep(1)
        #     print('Exit')
        #     sys.exit(0)
        print('dddd')
        rs, ws, xs = select(rlist, wlist, xlist, 1)
        print('after')
        for r in rs:
            print('ssss')
            if r is client:
                try:
                    print(1)
                    data = r.recv(date_rate*8).decode()
                    print(2)
                except BlockingIOError as e:
                    print(e)
                if not data:
                    print('no data')
                elif 'start' in data:
                    B = 5
                    r.send(request_falg.encode())
                    startime = time.time()
                    print("Initial finished,------value_B: ", B, 'startime: ', startime)
                elif 'exit' in data:
                    playtime = time.time() - startime
                    #计算播放片段，并更新
                    playB = int(playtime/8)
                    if playB >= 1:
                        startime += playB*8
                        B = B - playB
                    if B <= 0:
                        r.send(initial_falg.encode())
                        print("缓存数据为0，出现卡顿，现在需要重新初始化缓存！")
                    else:
                        r.send(request_falg.encode())
                        print("Next request, ------value_B: ", B, 'playtime: ', playtime)
                elif 'end' in data:
                    playtime = time.time() - startime
                    # 计算播放片段，并更新
                    playB = int(playtime / 8)
                    if playB >= 1:
                        startime += playB*8
                        B = B - playB + 1
                    else:
                        B += 1

                    if B <= 0:
                        r.send(initial_falg.encode())
                        print("缓存数据为0，出现卡顿，现在需要重新初始化缓存！")
                    elif B > 10:
                        r.send(stop_falg.encode())
                        print("we send a pause symbol to server, ask it to pause sending data!")
                    else:
                        r.send(request_falg.encode())
                        print("Next request, ------value_B: ", B, 'playtime: ', playtime)


if __name__ == '__main__':
    main(1024*50)