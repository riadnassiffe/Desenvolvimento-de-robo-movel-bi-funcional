'''
    ClienteUnoR4WiFi
'''
from cliente import Cliente
import struct
import socket
import builtins
import threading 
import sys
import time
import readline
import builtins
from erro import *
from comandos import *

'''
    Classe ClienteUnoR4Wifi

    Para mais detalhes é recomendado ler a documentação sobre a parte 
    do cliente no github

'''
class ClienteUnoR4Wifi(Cliente):
    
    def __init__(self, porta_cliente: int, porta_robo: int):
        super().__init__(porta_cliente, porta_robo)
        self._estado = 1
        self.valor = None

    def descoberta(self):
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_sock.bind(("", self._porta_cliente))
        udp_sock.settimeout(2.0)

        mensagem = b"UnoR4WiFi"

        while(True):
            udp_sock.sendto(mensagem, ("255.255.255.255", self._porta_robo))

            try:
                data, addr = udp_sock.recvfrom(1024)
                self._addr = addr[0]
                print(f"Robô respondeu: {data.decode()}")
                print(f"Endereço do robô: {self._addr}")
                break
            except socket.timeout:
                print("Robô não respondeu à descoberta.")
                time.sleep(0.5)
                
        udp_sock.close()

    def conectar(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self._socket.connect((self._addr, self._porta_robo))
        except socket.error as e:
            print(f"Erro ao conectar via TCP: {e}")
            sys.exit()

        self._socket.settimeout(2.0)

    def desconectar(self):
        try:
            self._socket.close()
        except:
            pass
        print("Conexão com Servidor Finalizada")

    def enviar_mensagem(self, mensagem:str):
        if self._estado and self._socket:
            try:
                self._socket.sendall(mensagem.encode())
            except OSError:
                pass
    
    def receber_mensagem(self, timeout=5.0):
            start = time.time()
            while True:
                if self.valor is not None:
                    val = self.valor
                    self.valor = None 
                    return val
                if time.time() - start > timeout:
                    return 999  
                time.sleep(0.01)  

    def escutar_servidor(self):
        buffer = b''  

        while self._estado:
            try:
                self._resposta = self._socket.recv(1024)

                if not self._resposta:
                    continue
                buffer += self._resposta

                while len(buffer) >= 4:
                    chunk = buffer[:4]
                    buffer = buffer[4:]
                    valor_float = struct.unpack('f', chunk)[0]
                    if (valor_float != 1.0):
                        self.valor = valor_float

            except socket.timeout:
                continue
            except OSError:
                break

    def iniciar_threads(self, n):

        match n:
            case(0):
                thread = threading.Thread(target=self.escutar_servidor, daemon=True)
                thread.start()

    def solicitar_status(self):
        pass
    
    def alterar_conexao(self):
        pass

    def testar_tempo_conexao(self, mensagem):
        pass
    
    def metodos(self):
        global enviar, receber, esperar
        enviar = self.enviar_mensagem
        receber = self.receber_mensagem
        esperar = time.sleep
         
    def executar(self):
        
        self.descoberta()
        self.conectar()
        self.metodos()
        self.iniciar_threads(0)
    
    
    