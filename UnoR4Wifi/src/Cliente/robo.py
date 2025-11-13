"""
Módulo da Fachada do Robô (robo.py)

Este arquivo abstrai toda a complexidade da conexão com o robô
(escondendo a classe 'ClienteUnoR4Wifi') e expõe funções
simples e globais que o 'main.py' pode utilizar.

O 'main.py' (o arquivo do usuário) deve importar
apenas deste módulo.
"""
#from clienteUnoR4WiFi import ClienteUnoR4Wifi
from comandos import *
import time
import sys

# --- Constantes de Conexão ---
PORTA_CLIENTE = 5005
"""Porta que este cliente (PC) usará para a descoberta UDP."""
PORTA_ROBO = 4210
"""Porta do Arduino (Servidor) para descoberta UDP e conexão TCP."""

# --- Variável Global de Conexão ---
_cliente = None
"""
Armazena a instância única do 'ClienteUnoR4Wifi' após a conexão.
As funções 'enviar' e 'receber' usam esta variável global.
"""

# --- Funções de Interface para o main.py ---

def enviar(comando: str):
    """Envia um comando de string para o robô.

    Verifica se a conexão (_cliente) existe e, em caso afirmativo,
    chama o método 'enviar_mensagem' do cliente.

    Args:
        comando (str): A string de comando (ex: "MF", "VS/120/120").
    """
    # Garante que o comando só seja enviado se a conexão (_cliente) foi estabelecida.
    if _cliente:
        _cliente.enviar_mensagem(comando)

def receber(timeout=5.0):
    """Espera e recebe um valor (float) do robô.

    Esta é uma função bloqueante. Ela espera até que a thread
    'escutar_servidor' (no cliente) preencha um valor.
    Chama 'verificar_erros' internamente (na classe Cliente).

    Args:
        timeout (float, optional): Tempo máximo de espera em segundos.
                                   Padrão é 5.0.

    Returns:
        float: O valor recebido do robô (ex: distância, status)
               ou 999 se o tempo estourar.
    """
    # Garante que a recepção só ocorra se a conexão (_cliente) existir.
    if _cliente:
        return _cliente.receber_mensagem(timeout)

# Atalho global para time.sleep, usado para consistência no main.py
esperar = time.sleep

def conectar_robo(cliente=None):
    """Inicializa e conecta ao robô.

    Esta função deve ser chamada uma vez no início do 'main.py'.
    Ela instancia o 'ClienteUnoR4Wifi' (escondendo as portas)
    e o armazena na variável global '_cliente'.
    Em seguida, chama o método 'executar()' do cliente para
    realizar a descoberta, conexão e iniciar a thread de escuta.
    """
    if cliente is None:
        # Garante que o usuário forneça uma classe de cliente válida.
        raise ValueError("Você precisa informar um cliente válido, no parametro de conectar_robo(ClienteUnoR4Wifi)")
    
    # Define a variável global _cliente para ser usada por outras funções do módulo.
    global _cliente
    print("Iniciando conexão com o robô")
    try:
        # Instancia o cliente com as portas padrão.
        _cliente = cliente(PORTA_CLIENTE, PORTA_ROBO)
        # O método executar lida com a descoberta, conexão e inicialização da thread.
        _cliente.executar()
       
        print("Robo pronto para ação")
    
    except Exception as e:
        # Em caso de falha na conexão, encerra o programa.
        print(f"Erro fatal ao conectar: {e}")
        sys.exit()

def desconectar_robo():
    """Desconecta do robô de forma segura.

    Esta função deve ser chamada no bloco 'finally' do 'main.py'.
    Ela envia um comando final de 'FINALIZAR' (para o Arduino)
    e, em seguida, fecha o socket de conexão.
    """
    if _cliente:
        print("Desligando robô")

        # Envia um comando para o Arduino saber que a conexão está sendo encerrada.
        _cliente.enviar_mensagem(FINALIZAR)
        # Fecha o socket e libera os recursos de rede.
        _cliente.desconectar()
        print("Robô desconectado.")