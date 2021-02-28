from framework.patterns import SingletonByName
from time import ctime, time


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log--->', text, ctime())




def debug(func):
    def inner(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print('DEBUG-------->', func.__name__, end - start)
        return result

    return inner