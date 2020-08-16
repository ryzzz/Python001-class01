#! -*- coding: utf-8 -*-

import time

'''
作业一：
容器序列：list, tuple, dict, collections.deque
扁平序列：str
可变序列：list, dict, collections.deque
不可变序列：str, tuple
'''

# 作业二
def my_map(func, iter):
    return [func(e) for e in iter]
print(my_map(str, [1,2,3,4]))

# 作业三
def timer(func):
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret
    return inner

@timer
def test_timer(t):
    start = time.time()
    time.sleep(t)
    print(time.time() - start)
test_timer(2)


