"""
Define a interface abstrata (Classe Base Abstrata - ABC) para um Cliente de Robô.

Esta classe serve como um "contrato", garantindo que qualquer classe de cliente
concreta implemente todos os métodos essenciais
para a comunicação, como conectar, enviar e receber.
"""

from abc import ABC, ABCMeta, abstractmethod
from erro import *

class Cliente(metaclass=ABCMeta):
    
    def __init__(self, porta_cliente:int, porta_robo:int):
        """Inicializa a classe base do Cliente.

        Args:
            porta_cliente (int): A porta de origem (deste script).
            porta_robo (int): A porta de destino (no robô).
        """
        self._porta_cliente = porta_cliente
        self._porta_robo = porta_robo
        self._addr = None
        self._socket = None
        self._resposta = None

    @property
    def resposta(self)->str:
        """Obtém a última resposta bruta recebida."""
        return str(self._resposta)

    @resposta.setter
    def resposta(self, new_resposta:str):
        """Define a última resposta (geralmente usado por threads de escuta)."""
        self._resposta = new_resposta

    @abstractmethod
    def conectar(self):
        """Método abstrato para estabelecer a conexão com o robô."""
        ...
        
    @abstractmethod
    def desconectar(self) -> None:
        """Método abstrato para encerrar a conexão com o robô."""
        ...

    @abstractmethod
    def alterar_conexao(self):
        """Método abstrato para modificar o estado da conexão (ex: reconectar)."""
        ...

    @abstractmethod
    def enviar_mensagem(self, mensagem:str) -> None:
        """Método abstrato para enviar uma string de comando ao robô."""
        ...
        
    @abstractmethod
    def receber_mensagem(self, timeout: float = 5.0) -> float:
        """Método abstrato para aguardar e receber uma resposta (float) do robô."""
        ...

    @abstractmethod    
    def testar_tempo_conexao(self,mensagem:str) -> float:
        """Método abstrato para medir o tempo de ida e volta de uma mensagem."""
        ...

    @abstractmethod
    def solicitar_status(self):
        """Método abstrato para requisitar o status atual do robô."""
        ...
        
    def verificar_erros(self, saida:int) -> int:
        """Verifica códigos de erro numéricos e levanta exceções Python.

        Args:
            saida (int): O código de status retornado pelo robô.

        Returns:
            int: O mesmo 'saida' se não for um código de erro conhecido.

        Raises:
            ErroPinoNaoConfigurado: Se o código for ERRO_0_PINO_NAO_CONFIGURADO.
            ErroValorParametroInvalido: Se o código for ERRO_1_PARAMETRO_INVALIDO.
            ErroComandoInvalido: Se o código for ERRO_2_COMANDO_INVALIDO.
        """
        if saida == ERRO_0_PINO_NAO_CONFIGURADO:
            raise ErroPinoNaoConfigurado()
        elif saida == ERRO_1_PARAMETRO_INVALIDO:
            raise ErroValorParametroInvalido()
        elif saida == ERRO_2_COMANDO_INVALIDO:
            raise ErroComandoInvalido()

        return saida