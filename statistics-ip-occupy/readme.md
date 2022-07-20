# Python脚本实现网络测试自动化

> **开发环境：**
>
> `Python` : `3.8.10`
>
> `OS` : `Windows 10 LTSC 2021 (x64) `
>
> `IDE` : `PyCharm 2022.1.3 (Professional Edition)`

---



##### 1.根据使用python的异或方法编写一段生成192.168.1.1~192.168.1.254的代码程序

> generate_ip_list.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_ip_list(start_ip, num):
    """
    通过位运算的方式，生成所需数量的IP地址集合
    :param start_ip: 起始IP
    :param num:     IP数量
    :return:   IP列表
    """
    # split_ip = map(int, start_ip.split('.'))
    # print(split_ip)
    # split_ip = list(split_ip)
    # 使用for循环，将传入的起始IP通过'.'拆分成int数组
    # 如：192.168.1.1拆分成[192,168,1,1]
    split_ip = [int(x) for x in start_ip.split('.')]
    # 返回IP集合结果
    ip_list = []
    # 通过for循环，遍历生成传入的IP数量，注意i的范围是0到num-1
    for i in range(num):
        # 将IP数组中的每个下标元素先进行相应的左移位运算，
        # 再进行按位或运算，最后生成IP对应的数字
        # 如：192.168.1.1转换为3232235777
        ip_int = split_ip[0] << 24 \
                 | split_ip[1] << 16 \
                 | split_ip[2] << 8 \
                 | split_ip[3]
        # 对IP数字进行循环加1，注意第一次i是0，
        # 所以IP数字加的是0，还是起始IP本身
        ip_int += i
        # 对IP数字先进行按位与运算，再进行相应的右移位运算，
        # 算出每个IP对应的拆分值，最后拼接成所需的IP字符串
        ip_addr = '%s.%s.%s.%s' % ((ip_int & 0xff000000) >> 24,
                                   (ip_int & 0x00ff0000) >> 16,
                                   (ip_int & 0x0000ff00) >> 8,
                                   (ip_int & 0x000000ff))
        # 将计算出的IP地址放入IP集合中
        ip_list.append(ip_addr)
    # 函数返回结果
    return ip_list


if __name__ == '__main__':
    # 生成IP段指定数量的IP地址
    print(get_ip_list('192.168.1.1', 254))

```

> **返回结果示例：**

![image-20220716185921611](C:\Users\wanghc\AppData\Roaming\Typora\typora-user-images\image-20220716185921611.png)



---



##### 2.使用python的xxx包对第一题生成的ip随机改变颜色，红色代表占用，绿色代表空闲，并将ip变换成\*，输出一个16*16的矩阵

> print_ip_occupy_matrix.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import threading
from queue import Queue

import generate_ip_list

# 定义线程数量
WORK_THREAD = 100
# 存放IP地址的队列，用于处理IP是否占用
IP_PING_QUEUE = Queue()
# 存放IP地址的队列，用于最后打印矩阵信息
IP_PRINT_QUEUE = Queue()
# 存放IP地址的队列，存放未被占用的IP
GREEN = Queue()
# 存放IP地址的队列，存放已被占用的IP
RED = Queue()


def store_ip_queue(start_ip, num):
    """
    存储IP地址到相关队列中
    :param start_ip: 起始IP
    :param num:     IP数量
    :return: None
    """
    # 通过调用第一步的函数生成IP集合
    ip_list = generate_ip_list.get_ip_list(start_ip, num)
    # 遍历IP结合并存放在对应的队列中
    for ip_element in ip_list:
        IP_PING_QUEUE.put(ip_element)
        IP_PRINT_QUEUE.put(ip_element)


def ping_ip_queue():
    """
    通过ping命令处理IP是否使用
    :return: None
    """
    # 对IP队列进行循环处理
    while not IP_PING_QUEUE.empty():
        # 获取IP地址
        ip_addr = IP_PING_QUEUE.get()
        # ping测试IP地址，-n：要发送的回显请求数，-w：等待每次回复的超时时间(毫秒)
        ping_response = os.popen(f"ping {ip_addr} -n 1 -w 100")
        # 超时返回信息因系统而异，当前使用的是Windows中文版系统
        timeout = '请求超时'
        # 如果返回中包含请求超时的字样，则代表未被占用，否则已被占用
        if timeout in ping_response.read():
            # 存放未被占用的IP地址
            GREEN.put(ip_addr)
        else:
            # 存放已被占用的IP地址
            RED.put(ip_addr)


def ping_threading():
    """
    启用多线程进行ping操作，加快处理速度
    :return: None
    """
    # 存放线程的集合
    threads = []
    # 根据配置的线程数，将配置后的线程放入线程集合
    for i in range(WORK_THREAD):
        # 定义线程工作
        thread = threading.Thread(target=ping_ip_queue)
        # 启动线程
        thread.start()
        # 放入线程集合
        threads.append(thread)
    # 遍历线程集合
    for thread in threads:
        # 等待直到线程终止
        thread.join()


def handle_occupy_result():
    """
    处理IP地址占用结果
    :return: IP地址是否占用的结果字典
    """
    # 存放结果的字典
    result = dict()
    # 处理未被占用的IP地址，并设为0
    while not GREEN.empty():
        result[(GREEN.get())] = 0
    # 处理已被占用的IP地址，并设为1
    while not RED.empty():
        result[(RED.get())] = 1
    # 返回结果
    return result


def print_matrix(start_ip, num, matrix):
    """
    打印矩阵信息
    :param start_ip: 起始IP
    :param num:      IP数量
    :param matrix:   矩阵行列数量
    :return: None
    """
    # 调用存储IP地址的函数
    store_ip_queue(start_ip, num)
    # 调用多线程处理的函数
    ping_threading()
    # 调用处理IP地址占用结果的函数
    result = handle_occupy_result()
    # 绘制矩阵信息，对指定矩阵的行和列进行双层遍历
    for row in range(matrix):
        for col in range(matrix):
            # 如果用于打印的队列信息为空，直接跳出所有循环
            if IP_PRINT_QUEUE.empty():
                break
            # 获取IP地址
            ip = IP_PRINT_QUEUE.get()
            # 获取IP地址占用信息
            occupy = result.get(ip)
            # 如果小于16列不需换行，col范围是0到15
            if col < 15:
                # 1代表已占用
                if occupy:
                    # 设置不换行并打印红色星号
                    print('\033[1;31m' + str('*  ') + '\033[0m', end="")
                # 0代表未占用
                else:
                    # 设置不换行并打印绿色星号
                    print('\033[1;32m' + str('*  ') + '\033[0m', end="")
            # 如果等于16列则需换行，col范围是0到15
            else:
                # 1代表已占用
                if occupy:
                    # 设置换行并打印红色星号
                    print('\033[1;31m' + str('*  ') + '\033[0m')
                # 0代表未占用
                else:
                    # 设置换行并打印绿色星号
                    print('\033[1;32m' + str('*  ') + '\033[0m')


if __name__ == '__main__':
    # 打印矩阵信息
    print_matrix('192.168.1.1', 254, 16)

```

> **返回结果示例：**

![](C:\Users\wanghc\AppData\Roaming\Typora\typora-user-images\image-20220717170252456.png)



---



##### 3.集团网络有多个网络，使用多进程方法，实现同时计算192.168.1.0/24、192.168.2.0/24、192.168.3.0/24三个网段的空闲ip个数

> calculate_idle_ip_number.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tmp import statistics_ip_occupy


def count_idle_ip(ip_list, num):
    """
    计算空闲IP数量
    :param ip_list: 需要计算的IP段集合
    :param num: IP段的IP数量
    :return: None
    """
    # 遍历需要计算的IP段集合，存放至IP地址队列中
    for ip in ip_list:
        # 调用存储IP地址的函数
        statistics_ip_occupy.store_ip_queue(ip, num)
    # 调用多线程处理的函数
    statistics_ip_occupy.ping_threading()
    # 调用处理IP地址占用结果的函数
    result = statistics_ip_occupy.handle_occupy_result()
    # 计算空闲IP数量
    idle_count = 0
    # 遍历IP地址是否占用的结果字典的所有value
    for value in result.values():
        # 如果是0则代表未占用
        if not value:
            # 空闲IP数量加1
            idle_count += 1
    # 打印计算的空闲IP总数
    print(idle_count)


if __name__ == '__main__':
    # 计算IP地址空闲数量
    count_idle_ip({'192.168.1.1', '192.168.2.1', '192.168.3.1'}, 254)

```

> **返回结果示例：**

![](C:\Users\wanghc\AppData\Roaming\Typora\typora-user-images\image-20220717170418347.png)

