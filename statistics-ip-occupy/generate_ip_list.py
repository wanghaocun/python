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
