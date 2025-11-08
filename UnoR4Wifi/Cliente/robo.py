from abc import ABC, ABCMeta, abstractmethod
from clienteUnoR4WiFi import ClienteUnoR4Wifi
from comandos import *
import time
import sys

PORTA_CLIENTE = 5005
PORTA_ROBO = 4210

_cliente = None

def enviar(comando: str):
    if _cliente:
        _cliente.enviar_mensagem(comando)

def receber(timeout=5.0):
    if _cliente:
        return _cliente.receber_mensagem(timeout)
    return 999

esperar = time.sleep

def conectar_robo():

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
    if _cliente:
        print("Desligando robô")

        _cliente.enviar_mensagem(FINALIZAR)
        _cliente.desconectar()
        print("Robô desconectado.")
