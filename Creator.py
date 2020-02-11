from abc import ABC, abstractmethod


class Creator(ABC):

    @abstractmethod
    def getActor(self):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def update(self, x, y):
        pass
