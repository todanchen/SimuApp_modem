import time
import socket
from select import select
import sys

def main(date_rate):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # client.connect(('124.160.127.162', 8001))
    # client.connect(('127.0.0.1', 8001))
    client.connect(('139.196.8.20', 8080))

    print('连接至服务器')
    connect(client, date_rate)


def connect(client, date_rate):

    initial_falg = 'initial' + ',' + str(date_rate)
    request_falg = 'request' + ',' + str(date_rate)
    stop_falg = 'stop'+ ',' + str(date_rate)
    client.send(initial_falg.encode())
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                print('no data')
            elif 'start' in data:
                B = 5
                client.send(request_falg.encode())
                startime = time.time()
                print("Initial finished,------value_B: ", B, 'startime: ', startime)
            elif 'exit' in data:
                playtime = time.time() - startime
                # 计算播放片段，并更新
                playB = int(playtime / 8)
                if playB >= 1:
                    startime += playB * 8
                    B = B - playB
                if B <= 0:
                    client.send(initial_falg.encode())
                    print("缓存数据为0，出现卡顿，现在需要重新初始化缓存！")
                else:
                    client.send(request_falg.encode())
                    print("Next request, ------value_B: ", B, 'playtime: ', playtime)
            elif 'end' in data:
                playtime = time.time() - startime
                # 计算播放片段，并更新
                playB = int(playtime / 8)
                if playB >= 1:
                    startime += playB * 8
                    B = B - playB + 1
                else:
                    B += 1

                if B <= 0:
                    client.send(initial_falg.encode())
                    print("缓存数据为0，出现卡顿，现在需要重新初始化缓存！")
                elif B > 1000:
                    client.send(stop_falg.encode())
                    print("we send a pause symbol to server, ask it to pause sending data!")
                else:
                    client.send(request_falg.encode())
                    print("Next request, ------value_B: ", B, 'playtime: ', playtime)

        except BlockingIOError as e:
            print(e)



if __name__ == '__main__':
    main(1024)