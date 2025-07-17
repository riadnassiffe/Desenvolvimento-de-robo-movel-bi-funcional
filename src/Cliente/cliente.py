'''
    Cliente

    Código que implementa a Classe cliente responsável por comunicar-se
    com o dispositivo executando o servidor em um Arduíno Uno. Utilize
    essa classe para conectar-se e trocar mensagens via blueetooth com
    o robô.
'''
from abc import ABC, ABCMeta, abstractmethod
import struct
from time import time
from erro import *

class Cliente(metaclass=ABCMeta):
    '''
        Descrição dos atributos
    
        @param self The object pointer
        @param addr Uma string que representa o endereço utilizado no robô para efetuar a comunicação.
        @param porta: Número inteiro que identifica a porta do computador que será utilizada para realizar a comunicação com o servidor.
    '''

    def __init__(self, addr:str, porta:int):
        self.__addr = addr
        self.__porta = porta
        self.__socket = None
        self.__resposta = None

    @property
    def resposta(self)->str:
        return str(self.__resposta)

    @resposta.setter
    def resposta(self, new_resposta:str):
        self.__resposta = new_resposta

    @abstractmethod
    def conectar(self):
        ...
        
    @abstractmethod
    def desconectar(self) -> None:
        ...
        
    @abstractmethod
    def enviar_mensagem(self, mensagem:str) -> None:
        ...
        
    @abstractmethod
    def get_resposta(self) -> str:
        ...

    def setup(self) -> None:
        pass

    @abstractmethod
    def acao(self) -> float:
        ...
    
    def solicitar_status(self):
        pass
        
    def executar(self):
        self.conectar()
        self.setup()
        while True:
            self.solicitar_status()
            self.acao()
            

    def veriricar_erros(self,saida:int)->int:
        if saida == 10000000:
            raise ErroPinoNaoConfigurado()
        elif saida == 10000001:
            raise ErroValorParametroInvalido()
        elif saida == 10000002:
            raise ErroComandoInvalido()

        return saida
        
        
    def testar_tempo_conexao(self,mensagem:str) -> float:
        '''
            Envia uma String para o servidor e calcula o tempo aproximado entre o envio e o 
            recebimento do retorno. Utilize esse método para verificar o tempo de resposta 
            aproximando de um comando enviado ao servidor. Atenção, esse método requer que 
            já exista uma conexão com o servidor.

            Parâmetros:
                mensagem - str - string que será enviada para o servidor

            Retorno:
                tempo - float - identifica o tempo gasto para enviar a mensagem e receber
                                retorno do servidor.
        '''
        tempo_inicial = time()
        self.enviar_mensagem(mensagem)
        self.get_resposta()
        return time() - tempo_inicial