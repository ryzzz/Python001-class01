#! -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod


class Zoo(object):
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

    def __init__(self, name, animal_type, body_type, character):
        super(Cat, self).__init__(animal_type, body_type, character)
        self.name = name
        self.is_tamable = True


if __name__ == '__main__':
    z = Zoo('时间动物园')
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    z.add_animal(cat1)
    have_cat = getattr(z, 'Cat')
    # print(have_cat)
