# week08 学习笔记

## 常用collections内置数据类型
### 命名元组
```python
from collections import namedtuple
Point = namedtuple('Ponit', ['x','y'])
p = Point(10, y=20)
p.x + p.y
p[0] + p[1]
x, y = p
```
### 计数器
```python
from collections import Counter
mystring = ['a','b','c','d','d','d','d','c','c','e']
# 取得频率最高的前三个值
cnt = Counter(mystring)
cnt.most_common(3)
cnt['b']
```
### 双向队列
```python
from collections import deque
d = deque('uvw')
d.append('xyz')
d.appendleft('rst')
```
## 常用函数操作和高阶函数
### 函数接收不定长参数
```python
def func(*args, **kargs):
    print(f'args: {args}')
    print(f'kargs: {kargs}')

func(123, 'xz', name='xvalue')
# args: [123, 'xz']
# kargs: {'name': 'xvalue'}
```
### 偏函数
```python
# 用于固定函数的某些参数
from functools import partial
def add(x, y):
    return x + y
add_1 = partial(add, 1)
add_1(10)
# 11
```
### 匿名函数
```python
k = lambda x:x+1
'''
相当于：
def k(x): 
    return x+1
'''
```
### map
```python
def square(x):
    return x**2
m = map(square, range(10))
next(m)
list(m)
'''
相当于
[square(x) for x in range(10)]
'''
```
### reduce
```python
from functools import reduce
def add(x, y):
    return x + y
reduce(add, [1, 3, 5, 7, 9])
#25
```
### filter
```python
def is_odd(n):
    return n % 2 == 1
list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# [1, 5, 9, 15]
```
### count
```python
from itertools import count
g = count()
next(g)
```
## 装饰器
```python
# 装饰器用于为函数添加额外功能，会在模块导入的时候自动运行
# 这个例子相当于把foo函数替换为了inner函数

def outer(func):
    def inner(*args,**kwargs):
				print(f'inner: {func.__name__}')
        ret = func(*args,**kwargs)
				return ret
    return inner

@outer
def foo(a,b,c):
		print(f'foo: {foo.__name__}')
    return (a+b+c)
    
print(foo(1,3,5))
# inner: foo
# foo: inner
# 9
```
### 带参数装饰器
```python
def outer_arg(bar):
    def outer(func):
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

# 相当于outer_arg('foo_arg')(foo)()
@outer_arg('foo_arg')
def foo(a,b,c):
    return (a+b+c)

print(foo(1,3,5))
# foo_arg
# 9
```
### 装饰器堆叠
```python
# 装饰器可以堆叠使用，依次从下到上实现

@classmethod
@synchronized(lock)
def foo(cls):
    pass

def foo(cls):
    pass

'''
相当于
foo2 = synchronized(lock)(foo)
foo3 = classmethod(foo2)
foo = foo3
'''
```
### 常用内置装饰器
#### warps
```python
# 不加warps时，foo被outer_arg装饰后，foo会被替换为inner，名字也会被替换
# warps可以让foo保留原来的名字

from functools import wraps

def outer_arg(bar):
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

@outer_arg('foo_arg')
def foo(a,b,c):
    return (a+b+c)
    
print(foo.__name__)
# foo
```
#### lru_cache
```python
# 需要频繁调用函数时，可以使用lru_cache
# lru_cache会将传入相同参数的相同函数的值进行缓存，避免重复调用，减少运行时间

import functools

@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
# 0.087
# 如果不用lru_cache则需要3.55秒
```
### 类装饰器
```python
# 在类中实现__call__，可以将类作为装饰器使用

class Count(object):
    def __init__(self,func):
        self._func = func
        self.num_calls = 0
    
    def __call__(self, *args, **kargs):
        self.num_calls += 1
        print(f'num of call is {self.num_calls}')
        return self._func(*args, **kargs)

@Count
def example():
    print('hello')

example()
# num of call is 1
```
### 使用装饰器装饰类
```python
# 装饰类其实是对类中某个方法进行装饰
# 这里是对类中display进行装饰，重写了功能

def decorator(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)
            
        def display(self):
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()
    return newClass

@decorator
class MyClass(object):
    def __init__(self, number):
        self.number = number
    # 重写display
    def display(self):
        print("number is",self.number)

six = MyClass(6)
for i in range(5):
    six.display()
```
## 对象协议(鸭子类型)
### 鸭子类型
- 一只动物走路像鸭子，我们就认为它就是鸭子。
- 一个Python对象，可以像字典一样去调用，我们就认为它就是字典。
### 对象协议
解决问题时，尽力使用Python原生对象类型，如字典。如果元素对象类型不能解决，而需要自己定义类时，就尽力将自己定义的类模拟成原生对象类型。

模拟原生对象类型，就需要满足该原生对象类型的对象协议。

对象协议由魔术方法来实现，模拟原生对象类型时尽力包含其所有魔术方法

### 常用对象协议
### 容器类型协议
- __str__ 打印对象时，默认输出该方法的返回值
- __getitem__、__setitem__、__delitem__ 字典索引操作
- __iter__ 迭代器
- __call__ 可调用对象协议
### 比较大小的协议
- __eq__
- __gt__
### 可哈希对象
- __hash__
### 上下文管理器
- __enter__
- __exit__

## 迭代器
### 生成器、迭代器、可迭代对象区别
- 可迭代对象(iterable)：包含 __getitem__ 或 __iter__ 方法
- 迭代器(iterator)：包含 __next__ 和 __iter__ 方法
- 生成器(Generator)：使用 yield 或 (i for i in range(3)) 来实现的迭代器
### 生成器
1. 在函数中使用 yield 关键字，可以实现生成器。
2. 使用  (i for i in range(3)) 也可以实现生成器
3. yield 和 return 不同，return 返回后，函数状态终止，yield 保持函数的执行状态，
返回后，函数回到之前保存的状态继续执行。
4. 函数被 yield 会暂停，局部变量也会被保存。
```python
def foo(n):
		for i in range(n):
			num = yield i
      print(num)

iterator = foo(3) # 定义生成器，这里没有执行
print(next(iterator)) # 第一次迭代只能传入None，next()等价于iterator.send(None)
											# 因为第一次迭代时函数是从头开始执行，这时还没有变量来接收传入的值
# 0
print(iterator.send('haha')) # 第二次就可以传入非None值，因为函数是从 num = 传入值开始执行的 
# haha
# 1
print(next(iterator)) # next()等价于iterator.send(None)
# None
# 2
print(next(iterator)) # 生成器消耗完后进行迭代会报错，可使用iterator = foo(3)重新定义生成器 
# StopIteration
```
### 常用内置迭代器

#### 计数器

```python
import itertools

count = itertools.count()
next(count)
# 0
next(count)
# 1
next(count)
# 2
```

#### 循环遍历

```python
import itertools

cycle = itertools.cycle(('yes', 'no'))
next(cycle)
# yes
next(cycle)
# no
next(cycle)
# yes
next(cycle)
# no
```
#### 重复
```python
import itertools

repeat = itertools.repeat(10, times=2)
next(repeat)
# 10
next(repeat)
# 10
next(repeat)
# StopIteration
```
### 深度迭代
```python
# 迭代时遇到可迭代对象时，对可迭代对象继续进行迭代

import itertools

for j in itertoos.chain('ABC'):
    print(j)
# A
# B
# C

# Python3.3 后可以使用 yield from 来实现相同功能
def chain(*iterables):
    for i in iterables:
        yield form i
list(chain('ABC'))
['A', 'B', 'C']
```
## 协程
### 协程与线程的区别
- 协程是异步的，线程是同步的
- 协程是非抢占式的，线程是抢占式的
- 线程是被动调度的，协程是主动调度的
- 协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器
- 协程是用户级的任务调度，线程是内核级的任务调度
- 协程适用于 IO 密集型程序，不适用于 CPU 密集型程序的处理
### 协程实现方式
python3.4 的方式
```python
# python3.4 支持事件循环方法
import asyncio

@asyncio.coroutine
def py34_func():
    yield from sth()
```
python3.5 的方式
```python
# python3.5 增加async await
async def py35_func():
    await sth()
'''
注意： await 接收的对象必须是awaitable对象
awaitable 对象定义了__await__()方法awaitable 
对象有三类
1 协程 coroutine
2 任务 Task
3 未来对象 Future
'''
```
例子
```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(3)
    print('world')

# asyncio.run()运行最高层级的conroutine
# 会先将main函数进行注册，然后异步执行main函数。当main函数产生结构时，再去回调main函数。
asyncio.run(main())
# hello
# sleep 3 second
# world
```
### 协程和进程配合
```python
from multiprocessing import Pool
import asyncio
import time

async def test(time):
    await asyncio.sleep(time)

async def main(num):
    start_time = time.time()
    tasks = [asyncio.create_task(test(1)) for proxy in range(num)]
    [await t for t in tasks]
    print(time.time() - start_time)

def run(num):
    asyncio.run(main(num))

if __name__ == "__main__":
    start_time = time.time()
    p = Pool()
    for i in range(4):
        p.apply_async(run, args=(2500,))
    p.close()
    p.join()
    print(f'total {time.time() - start_time}')
```

## 遇到的问题
iterator.send(1)

TypeError: can't send non-None value to a just-started generator

原因：yield 第一次迭代不能传入非None值