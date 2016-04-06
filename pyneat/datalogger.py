from abc import ABCMeta
from abc import abstractmethod

class DataObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def experiment(self, name, conf):
        pass

    @abstractmethod
    def population(self, pop_index):
        pass

    @abstractmethod
    def generation(self, gen_index, species):
        pass

class DataLogger(object):
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def notify_experiment(self, name, conf):
        for o in self.__observers:
            o.experiment(name, conf)

    def notify_population(self, pop_index):
        for o in self.__observers:
            o.population(pop_index)

    def notify_generation(self, gen_index, species):
        for o in self.__observers:
            o.generation(gen_index, species)
