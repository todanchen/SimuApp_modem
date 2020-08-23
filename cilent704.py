import time
import socket
from select import select
import traceback
import threading
import logging
from logging import handlers

#This function is used to download video data
def download():
    global date_rate
    global B
    global cycle_flag
    global start_flag
    global starttime
    global lock

    request_falg = 'request' + ',' + str(date_rate)
    kflag = False
    print('th1')
    while cycle_flag:
        #Connetc the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        rlist = [client]
        wlist = []
        xlist = []
        conserver = False
        client.settimeout(5)
        #connect the server
        try:
            client.connect(('124.160.127.162', 6543))
            # client.connect(('127.0.0.1', 8001))
            conserver = True
            # print('Connect the video server!')
            logging.info("Connect the video server!")
        except OSError:
            # print('Not network!')
            logging.error('Not network!',traceback.format_exc())
            time.sleep(1)
        except:
            # traceback.print_exc()
            mess = traceback.format_exc()
            logging.error(mess)
        # Request the first video clip data
        if conserver:
            try:
                client.send(request_falg.encode())
                kflag = True
            except:
                # traceback.print_exc()
                mess = traceback.format_exc()
                logging.error(mess)

        #Cycle download the video clip data
        while kflag:
            rs, ws, xs = select(rlist, wlist, xlist, 1)
            for r in rs:
                if r is client:
                    r.settimeout(2)
                    try:
                        data = r.recv(date_rate).decode()
                    except:
                        #If there's error,we need to reconnect the Dlink
                        r.close()
                        rlist.remove(r)
                        kflag = False
                        # traceback.print_exc()
                        mess = traceback.format_exc()
                        logging.error(mess)
                        break

                    if not data:
                        r.close()
                        rlist.remove(r)
                        kflag = False
                        # traceback.print_exc()
                        mess = traceback.format_exc()
                        logging.error(mess)
                        break
                    elif 'next' in data:
                        get_B = int(data.split(',')[1])
                        #we need to acquire the thread lock before change the Shared variable
                        lock.acquire()
                        B += get_B
                        if start_flag == False:
                            start_flag = True
                            starttime = time.time()+1
                        lock.release()
                        # print('Now time: ', time.asctime(time.localtime(time.time())), ' Video_clip size: ', get_B, ' Buffer size: ', B)
                        #Determine whether the buffer has reached threshold
                        if B > 30:
                            # print('Pause data transmit for: ', B-29, 's.')
                            logging.info('Pause data transmit for: '+str(B-29)+'s.')
                            time.sleep(B-29)
                        # print("Next request")
                        logging.info("Next data clip request!")
                        r.settimeout(1)
                        try:
                            r.send(request_falg.encode())
                        except:
                            # traceback.print_exc()
                            r.close()
                            rlist.remove(r)
                            kflag = False
                            mess = traceback.format_exc()
                            logging.error(mess)
                            break



            # Define exit time
            if (time.time() - starttime) > 3000:
                logging.info("The program exits normally!")
                client.close()
                rlist.remove(client)
                kflag = False
                cycle_flag = False

#This function is used to simulate playing video data so that we can determine if the video is stuck
def video_play():
    global B
    global cycle_flag
    global start_flag
    global starttime
    global lock
    print('th2')
    while cycle_flag:
        time.sleep(0.5)
        if start_flag:
            # Calculate the video data consumption
            # print('Video plays time: ', time.asctime(time.localtime(starttime)))
            # logging.info('Video plays!')
            playB = int(time.time() - starttime)
            lock.acquire()
            if playB >= 1:
                starttime += playB
                B = B - playB
                # print('REDUCE! B Buffer Size: ', B)
                mess = 'Video plays! B Buffer Size: ' + str(B)
                logging.info(mess)
            #Determine whether there's the playable video data
            if B < 1:
                B = 0
                start_flag = False
                # print('Pause Time: ', time.asctime(time.localtime(time.time())),  '. The videos need to load data!')
                logging.warning("\033[31;40mThe current video freezes and needs to load data!\033[0m")
            lock.release()
        else:
            # print('Not video data!')
            time.sleep(1)

def log():
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(threadName)s - %(levelname)s: %(message)s')

    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    log_file = './log/{}video_test.txt'.format(current_time)
    # fileHandler = handlers.TimedRotatingFileHandler(filename=log_file, when='H')
    fileHandler = handlers.RotatingFileHandler(filename=log_file)
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(formatter)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler((streamHandler))


if __name__ == '__main__':
    log()
    #The data bit rate
    date_rate = 1024*1024*5
    #Buffer size
    B = 0
    #The video start playing flag
    start_flag = False
    cycle_flag = True
    # The video start playing time
    starttime = time.time()
    #Get the thread lock
    lock = threading.Lock()
    th1 = threading.Thread(target=download, name="video_download")
    th2 = threading.Thread(target=video_play, name="video_play")
    th1.start()
    th2.start()
    th1.join()
    th2.join()
