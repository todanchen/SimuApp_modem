import time
import socket
from select import select
import traceback

def main(date_rate):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            client.connect(('124.160.127.162', 6003))
            break
        except:
            pass
    print('连接至服务器')

    connect(client, date_rate)


def connect(client, date_rate):
    rlist = [client]
    wlist = []
    xlist = []
    connectime = time.time()
    count = 0

    initial_falg = 'initial' + ',' + str(date_rate)
    request_falg = 'request' + ',' + str(date_rate)

    while True:
        try:
            client.send(initial_falg.encode())
            break
        except:
            pass
    print('发送数据')

    while True:
        rs, ws, xs = select(rlist, wlist, xlist, 1)
        for r in rs:
            if r is client:
                try:
                    data = r.recv(date_rate).decode()
                except:
                    traceback.print_exc()
                    break

                if not data:
                    print('no data')
                    pass
                elif 'start' in data:
                    B = int(data.split(',')[1])
                    r.send(request_falg.encode())
                    star_time = time.time()
                    print("Initial finished,------value_B: ", B, 'star_time: ', star_time)

                elif 'next' in data:
                    print(data)
                    playtime = time.time() - star_time
                    # 计算播放片段，并更新
                    playB = int(playtime)
                    if playB >= 1:
                        star_time += playB
                        B = B - playB

                    get_B = int(data.split(',')[1])
                    B += get_B
                    if B <= 0:
                        count += 1
                        r.send(initial_falg.encode())
                        print("缓存数据为0，出现卡顿，现在需要重新初始化缓存！")
                    elif B > 80:
                        print('Pause data transmit for: ', get_B, 's.')
                        time.sleep(get_B)
                        r.send(request_falg.encode())
                        print("Next request, ------value_B: ", B, 'playtime: ', playtime)
                    else:
                        r.send(request_falg.encode())
                        print("Next request, ------value_B: ", B, 'playtime: ', playtime)


        # 时间到退出该测试
        endtime = time.time() - connectime
        if endtime > 3000:
            print('卡顿次数为：', count)
            try:
                client.send('Exit,0000'.encode())
            except:
                pass
            time.sleep(1)
            break


if __name__ == '__main__':
    # date_rates = [1024*100, 1024*200, 1024*500, 1024*600, 1024*700, 1024*800, 1024*900, 1024*1000, 1024*1100,
    #               1024*1200, 1024*1300, 1024*1400, 1024*1500, 1024*1600, 1024*1700, 1024*1800, 1024*1900,
    #               1024*2000, 1024*2100,]
    # for rate in date_rates:
    #     main(rate)
    #     print('test video data finished')
    #     time.sleep(2)
    #夺命地铁720
    main(1024*180)