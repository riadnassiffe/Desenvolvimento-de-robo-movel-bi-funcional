'''
    Cliente
'''
from cliente import Cliente
import struct
import socket
import threading
import sys
import time
import readline
from erro import *


class ClienteUnoR4Wifi(Cliente):
    '''
        Descrição dos atributos

    '''

    def __init__(self, porta_cliente: int, porta_robo: int):
        super().__init__(porta_cliente, porta_robo)
        self._T1 = 0
        self._T2 = 0
        self._estado = 1

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
                print(f"Robô respondeu via UDP: {data.decode()}")
                print(f"Endereço do robô: {self._addr}")
                break
            except socket.timeout:
                print("Robô não respondeu à descoberta (UDP).")
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
        self._socket.close()
        sys.exit()

    def enviar_mensagem(self, mensagem:str):
        self._T1 = time.perf_counter()
        self._socket.sendall((mensagem).encode())
    
    def receber_mensagem(self):
        self._resposta = self._socket.recv(1024)
        self._T2 = time.perf_counter()

    def escutar_servidor(self):
        while True:
            try:
                self.receber_mensagem()
                data = self._resposta
                rtt = 0
                if (self._T1 != 0):
                    rtt = (self._T2 - self._T1) * 1000  # milissegundos

                current_line = readline.get_line_buffer()
                sys.stdout.write('\r' + ' ' * (len(current_line)+30) + '\r')
                try:
                    decoded = data.decode()
                    print(f"[Robô]: {decoded.strip()} | RTT: {rtt:.2f} ms")
                except UnicodeDecodeError:
                    valor_float = struct.unpack('f', data)[0]
                    print(f"[Robô]: {valor_float:.2f} (binário) | RTT: {rtt:.2f} ms")

                sys.stdout.write(f"Comando: {current_line}")
                sys.stdout.flush()

                self._T1 = 0 
                self._T2 = 0
            except socket.timeout:
                continue
            except OSError:
                break

    def escutar_cliente(self):
        while True:
            comando = input()
            if comando.lower() == "sair":
                self._estado = 0
                break
            else:
                self.enviar_mensagem(comando)
        self.desconectar()

            

    def get_resposta(self) -> float:
        return self._resposta

    def solicitar_status(self):
        print("status\n")
    
    def alterar_conexao(self):
        print("conexao\n")

    def testar_tempo_conexao(self, mensagem):
        print("tempo\n")

    def setup(self) -> None:
        while (True):
            comando = input()
            if comando.lower() == "*":
                self._T1 = time.perf_counter()
                self.enviar_mensagem(comando)
                break
            self._T1 = time.perf_counter()
            self.enviar_mensagem(comando)

    def executar(self):
        
        self.descoberta()
        self.conectar()

        thread = threading.Thread(target=self.escutar_servidor, daemon=True)
        thread.start()

        self.setup()

        thread1 = threading.Thread(target=self.escutar_cliente, daemon=True)
        thread1.start()

        while self._estado:
            #self.solicitar_status()
            #self.alterar_conexao()
            self.acao()

        self.desconectar()
    
    def acao(self) -> float:
        comando = "VS/150/150"
        self.enviar_mensagem(comando)
        time.sleep(5)
        
        comando = "MF"
        self.enviar_mensagem(comando)
        time.sleep(5)
        
        comando = "MP"
        self.enviar_mensagem(comando)
        time.sleep(5)
        
        comando = "MT"
        self.enviar_mensagem(comando)
        time.sleep(5) 
    
        

# Execução de um exemplo de troca de mensagens entre cliente e servidor
if __name__ == "__main__":
    
    PORTA_CLIENTE = 5005
    PORTA_ROBO = 4210

    cliente = ClienteUnoR4Wifi(PORTA_CLIENTE, PORTA_ROBO)

    cliente.executar()

