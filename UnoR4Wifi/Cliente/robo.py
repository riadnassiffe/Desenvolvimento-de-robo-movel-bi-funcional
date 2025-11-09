"""
Módulo da Fachada do Robô (robo.py)

Este arquivo abstrai toda a complexidade da conexão com o robô
(escondendo a classe 'ClienteUnoR4Wifi') e expõe funções
simples e globais que o 'main.py' pode utilizar.

O 'main.py' (o arquivo do usuário) deve importar
apenas deste módulo.
"""
from clienteUnoR4WiFi import ClienteUnoR4Wifi
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
As funções 'enviar' e 'receber' usam esta variável.
"""

# --- Funções de Interface para o main.py ---

def enviar(comando: str):
    """Envia um comando de string para o robô.

    Verifica se a conexão (_cliente) existe e, em caso afirmativo,
    chama o método 'enviar_mensagem' do cliente.

    Args:
        comando (str): A string de comando (ex: "MF", "VS/120/120").
    """
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
    if _cliente:
        return _cliente.receber_mensagem(timeout)

# Atalho global para time.sleep, usado para consistência no main.py
esperar = time.sleep

def conectar_robo():
    """Inicializa e conecta ao robô.

    Esta função deve ser chamada uma vez no início do 'main.py'.
    Ela instancia o 'ClienteUnoR4Wifi' (escondendo as portas)
    e o armazena na variável global '_cliente'.
    Em seguida, chama o método 'executar()' do cliente para
    realizar a descoberta, conexão e iniciar a thread de escuta.
    """
    global _cliente
    print("Iniciando conexão com o robô")
    try:
        _cliente = ClienteUnoR4Wifi(PORTA_CLIENTE, PORTA_ROBO)
        _cliente.executar()
       
        print("Robo pronto para ação")
    
    except Exception as e:
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

        _cliente.enviar_mensagem(FINALIZAR)
        _cliente.desconectar()
        print("Robô desconectado.")