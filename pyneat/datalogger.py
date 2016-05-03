from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime

class DataObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def experiment(self, name, conf, dt):
        pass

    @abstractmethod
    def experiment_end(self, dt):
        pass

    @abstractmethod
    def population(self, pop_index):
        pass

    @abstractmethod
    def generation(self, gen_index, species):
        pass

    @abstractmethod
    def progress(self, progress, message):
        pass

class DataLogger(object):
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def notify_experiment(self, name, conf, dt=datetime.now()):
        for o in self.__observers:
            o.experiment(name, conf, dt)

    def notify_experiment_end(self, dt=datetime.now()):
        for o in self.__observers:
            o.experiment_end(dt)

    def notify_population(self, pop_index):
        for o in self.__observers:
            o.population(pop_index)

    def notify_generation(self, gen_index, species):
        for o in self.__observers:
            o.generation(gen_index, species)

    def notify_progress(self, progress=None, message=None):
        for o in self.__observers:
            o.progress(progress, message)
