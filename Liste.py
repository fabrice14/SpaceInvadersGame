from typing import TypeVar, Generic

T = TypeVar('T')


class Liste(Generic[T]):

    def __init__(self):
        self.__liste = []

    def addElement(self, element: T):
        self.__liste.append(element)

    def removeAllElement(self):
        self.__liste.clear()

    @property
    def list(self):
        return self.__liste

    @list.setter
    def list(self, a):
        self.__liste = a

    def clearListe(self):
        newList = []
        if self.__liste:
            for element in self.__liste:
                if element.getStatus() == 1:
                    newList.append(element)
        return newList
