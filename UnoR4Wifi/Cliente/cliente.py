'''
    Cliente

    Código que implementa a Classe cliente responsável por comunicar-se
    com o dispositivo executando o servidor em um Arduíno Uno. Utilize
    essa classe para conectar-se e trocar mensagens com o robô.

    Futuramente talvez seria melhor criar uma pra WiFi e outra pra Bluetooth
'''
from abc import ABC, ABCMeta, abstractmethod
import struct
from time import time
from erro import *

class Cliente(metaclass=ABCMeta):
    
    def __init__(self, porta_cliente:int, porta_robo:int):
        self._porta_cliente = porta_cliente
        self._porta_robo = porta_robo
        self._addr = None
        self._socket = None
        self._resposta = None

    @property
    def resposta(self)->str:
        return str(self._resposta)

    @resposta.setter
    def resposta(self, new_resposta:str):
        self._resposta = new_resposta

    @abstractmethod
    def conectar(self):
        ...
        
    @abstractmethod
    def desconectar(self) -> None:
        ...

    @abstractmethod
    def alterar_conexao(self):
        ...

    @abstractmethod
    def enviar_mensagem(self, mensagem:str) -> None:
        ...
        
    @abstractmethod
    def receber_mensagem(self, timeout: float = 5.0) -> float:
        ...

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def acao(self) -> float:
        ...
    
    @abstractmethod    
    def testar_tempo_conexao(self,mensagem:str) -> float:
        ...

    @abstractmethod
    def solicitar_status(self):
        ...
        
    def executar(self):
        self.conectar()
        self.setup()
        while True:
            self.acao()
            

    def veriricar_erros(self,saida:int)->int:
        if saida == 10000000:
            raise ErroPinoNaoConfigurado()
        elif saida == 10000001:
            raise ErroValorParametroInvalido()
        elif saida == 10000002:
            raise ErroComandoInvalido()

        return saida
        
  