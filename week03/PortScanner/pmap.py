# -*- coding: utf-8 -*-

import time
import json
import socket
import argparse
import platform
import subprocess
from ipaddress import ip_address
from collections import defaultdict
from multiprocessing.pool import Pool as ProcPool
from multiprocessing.dummy import Pool as ThreadPool

'''
pip install argparse
python3
'''

PORT_RANGE = [1, 1024]


def ip_format(ipaddress):
    ip_parser = ipaddress.split('-')
    try:
        start = ip_address(ip_parser[0])
        end = ip_address(ip_parser[-1])
    except:
        raise Exception('IP address format error.')
    if start > end:
        raise Exception('IP segment format error.')
    ip_list = []
    while start <= end:
        ip_list.append(str(start))
        start += 1
    return ip_list


def ping_test(ip):
    ret = subprocess.call("ping -n 4 {} > nul".format(ip),
                          shell=True) if platform.system() == "Windows" else subprocess.call(
                          "ping -c 4 {} > /dev/null".format(ip), shell=True)
    return False if ret else True


def port_test(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except socket.error:
        return False


def scan(ip, port=None):
    if ping_test(ip):
        if port:
            if port_test(ip, port):
                return ip, port
        return ip


def run(ipaddress, concurrency, mode, function, write, view):
    ip_list = ip_format(ipaddress)
    if mode == 'thread':
        pool = ThreadPool(concurrency)
    else:
        pool = ProcPool(concurrency)
    t1 = time.time()
    result_list = pool.map(scan, ip_list)
    t2 = time.time()
    available_ip_port = list(filter(None, result_list))
    if view:
        print('ping time: {}'.format(t2 - t1))
    if function == 'tcp':
        ip_port_iter = ((ip, port) for ip in available_ip_port for port in range(PORT_RANGE[0], PORT_RANGE[-1] + 1))
        t3 = time.time()
        result_list = pool.starmap(scan, ip_port_iter)
        t4 = time.time()
        available_ip_port = defaultdict(list)
        for result in result_list:
            if isinstance(result,tuple):
                available_ip_port[result[0]].append(result[1])
        if view:
            print('tcp time: {}'.format(t4 - t3))
    pool.close()
    pool.join()
    print(available_ip_port)
    if write:
        with open(write, 'w+') as f:
            json.dump(available_ip_port, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port Scanner.')
    parser.add_argument('-n', '--number', default=1, type=int, help='Number of concurrency.')
    parser.add_argument('-m', '--mode', default='thread', choices=['thread', 'proc'],
                        help='"ping": Scans for available IP. "tcp": Scans for available ports.')
    parser.add_argument('-f', '--function', default='ping', choices=['ping', 'tcp'],
                        help='"ping": Scans for available IP. "tcp": Scans for available ports.')
    parser.add_argument('-ip', '--ipaddress', default='127.0.0.1',
                        help='IP address or IP segment. eg: 192.168.0.1-192.168.0.100')
    parser.add_argument('-w', '--write', help='Output json file path.')
    parser.add_argument('-v', '--view', action='store_true', help='Check scanner run time.')
    args = parser.parse_args()

    run(args.ipaddress, args.number, args.mode, args.function, args.write, args.view)
