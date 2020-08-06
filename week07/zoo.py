#! -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod


class Zoo(object):
    animal_instance = {}

    def __init__(self, name):
        self.name = name

    def add_animal(cls, animal_instance):
        setattr(cls, animal_instance.__class__.__name__, True)

    def __getattr__(self, item):
        return False


class Animal(ABC):
    @abstractmethod
    def __init__(self, animal_type, body_type, character):
        self.animal_type = animal_type
        self.body_type = body_type
        self.character = character
        self.is_dangerous = True if (body_type == '中' or body_type == '大') and character == '凶猛' else False


class Cat(Animal):
    sound = '喵'

    _instance = None

    def __new__(cls, *args, **kargs):
        if not cls._instance:
            cls._instance = super(Animal, cls).__new__(cls)
        return cls._instance

    def __init__(self, name, animal_type, body_type, character):
        super(Cat, self).__init__(animal_type, body_type, character)
        self.name = name
        self.is_tamable = True


if __name__ == '__main__':
    z = Zoo('时间动物园')

    # animal = Animal('食肉', '小', '温顺')
    # TypeError: Can't instantiate abstract class Animal with abstract methods __init__

    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    cat2 = Cat('大花猫 2', '食肉', '小', '温顺')
    # cat1 和 cat2 为相同实例
    print(cat1 is cat2)

    # cat1 叫
    print(cat1.sound)

    # 添加动物，有猫时getattr(z, 'Cat')返回True，没有时返回False
    print(getattr(z, 'Cat'))
    z.add_animal(cat1)
    print(getattr(z, 'Cat'))
