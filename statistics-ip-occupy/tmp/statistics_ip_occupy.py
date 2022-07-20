#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  @explain : statistics ip occupy
  @since   : 2022-07-16
  @author  : wanghaocun
  @software: JB-PyCharm
  @file    : print_ip_occupy_matrix.py
"""

import os
import threading
import time
from functools import wraps
from queue import Queue

from memory_profiler import profile

ip_list = ['192.168.1.' + str(i) for i in range(1, 255)]

WORK_THREAD = 100
IP_QUEUE = Queue()
IP_QUEUE_CYCLE = Queue()
# ip_list.append('www.baidu.com')
for i in ip_list:
    IP_QUEUE.put(i)
    IP_QUEUE_CYCLE.put(i)

""" 写一个装饰器，进行函数消耗时间的统计"""


def timer(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        start = time.time()
        func(*arg, **kwargs)
        end = time.time()
        print(f'func_name：{func.__name__}, time consuming：{round(end - start, 2)} S ')
        return func

    return wrapper


green = Queue()  # 这个是放没有被占用的IP
red = Queue()  # 这个是放被占用的IP


def ping_ip_queue():
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()
        res = os.popen(f"ping {ip} -n 1 -w 1")
        if '请求超时' in res.read():
            green.put(ip)
        else:
            red.put(ip)


"""profile 是一个内存分析函数，最近法装饰"""


@timer
@profile
def ping_threading():
    threads = []
    for i in range(WORK_THREAD):
        thread = threading.Thread(target=ping_ip_queue)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


if __name__ == '__main__':

    ping_threading()
    res = dict()

    while not green.empty():
        res[(green.get())] = 1
    while not red.empty():
        res[(red.get())] = 0

    print('\n')
    print("".center(240, '='))
    print(">>> 内网IP测试结果 <<<".center(230, ' '))
    print("".center(240, '='))

    for col in range(16):
        for row in range(16):
            if IP_QUEUE_CYCLE.empty():
                break
            ip = IP_QUEUE_CYCLE.get()
            if row < 15:
                if res.get(ip):
                    # print('\033[1;32m' + str('*  ') + '\033[0m', end="")
                    print('\033[1;32m' + str(ip).ljust(15, ' ') + '\033[0m', end="")
                else:
                    # print('\033[1;31m' + str('*  ') + '\033[0m', end="")
                    print('\033[1;31m' + str(ip).ljust(15, ' ') + '\033[0m', end="")
            else:
                if res.get(ip):
                    # print('\033[1;32m' + str('*  ') + '\033[0m')
                    print('\033[1;32m' + str(ip).ljust(15, ' ') + '\033[0m')
                else:
                    # print('\033[1;31m' + str('*  ') + '\033[0m')
                    print('\033[1;31m' + str(ip).ljust(15, ' ') + '\033[0m')

    print()
    print("".center(240, '='))
    print(">>>（\033[1;32m绿色\033[0m未占用，\033[1;31m红色\033[0m已占用）<<<".center(238, ' '))
    print("".center(240, '='))

    # print(res)
    #
    # print('This is a \033[1;35m test \033[0m!')
    # print('This is a \033[1;32;43m test \033[0m!')
    # print('\033[1;33;44mThis is a test !\033[0m')
    # while not green.empty():
    #     res[(green.get())] = 1
    #     print('\033[1;32m' + res + '\033[0m]')
    #
    # while not red.empty():
    #     res[(red.get())] = 0
    #     print('\033[1;31m' + res + '\033[0m]')
