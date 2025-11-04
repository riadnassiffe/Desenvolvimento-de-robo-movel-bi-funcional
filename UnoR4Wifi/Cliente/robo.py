from abc import ABC, ABCMeta, abstractmethod
import struct
from time import time
from erro import *

class Robo(metaclass=ABCMeta):

    @abstractmethod
    def acao(self) -> float:
        ...