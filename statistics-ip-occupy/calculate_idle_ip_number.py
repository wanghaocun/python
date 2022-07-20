#!/usr/bin/env python
# -*- coding: utf-8 -*-

import print_ip_occupy_matrix


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
    result = print_ip_occupy_matrix.handle_occupy_result()
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
