import queue
import threading
import time
import json
import sys

MYSQL_CONFIG={"host":'127.0.0.1',
            "port":3306,
            "user":'wxwmodder',
            "password":'sxmc321',
            "db":'scrapy01'}
def getMySQLConfig():
    return MYSQL_CONFIG
L=queue.Queue()
L2=queue.Queue()
task_list=[]

def putElement(element):
    time.sleep(3)
    L.put(element)

if __name__ == "__main__":
    print(getMySQLConfig()['host'])

    # print(sys.path)
    # for task in range(1,10):
    #     t=threading.Thread(target=putElement,args=({"数字":task},))
    #     task_list.append(t)
    #     t.start()
    # for task in range(1,10):
    #     t=threading.Thread(target=putElement,args=({"数字2":task},))
    #     task_list.append(t)
    #     t.start()
    # for i in task_list:
    #     i.join()
    # print(L.qsize())

    # list_2=[L.get() for i in range(1,L.qsize())]
    
    # [L2.put(i) for i in list_2]

    # print([L2.get() for i in range(1,L2.qsize())])