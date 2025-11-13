"""
Define a interface abstrata para um Cliente de Robô.

Esta classe serve como um "contrato", garantindo que qualquer classe de cliente concreta implemente todos os métodos essenciais para a comunicação, como conectar, enviar e receber.
"""

from abc import ABC, ABCMeta, abstractmethod
from erro import *

class Cliente(metaclass=ABCMeta):
    """Essa classe é uma interface que deve ser herda por outra classe que deve implementar
    as especificidades de comunicação com a placa que controla o robô.

    """
    
    def __init__(self, porta_cliente:int, porta_robo:int):
        """Inicializa a classe base do Cliente.

            :param porta_cliente (int): A porta de origem (deste script).
            :param porta_robo (int): A porta de destino (no robô).
        """
        self._porta_cliente = porta_cliente # Porta UDP para descoberta
        self._porta_robo = porta_robo       # Porta do servidor no robô (UDP e TCP)
        self._addr = None                   # Endereço IP do robô, a ser descoberto
        self._socket = None                 # Socket TCP para comunicação principal
        self._resposta = None               # Armazena a última resposta bruta recebida

    @property
    def resposta(self)->str:
        """Obtém a última resposta recebida."""
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
        # Compara o valor de saída com os códigos de erro predefinidos.
        if saida == ERRO_0_PINO_NAO_CONFIGURADO: # Código 10000000.0
            raise ErroPinoNaoConfigurado()
        elif saida == ERRO_1_PARAMETRO_INVALIDO: # Código 10000001.0
            raise ErroValorParametroInvalido()
        elif saida == ERRO_2_COMANDO_INVALIDO:   # Código 10000002.0
            raise ErroComandoInvalido()

        # Se não for um erro, retorna o valor original.
        return saida