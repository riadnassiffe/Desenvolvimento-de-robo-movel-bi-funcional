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
from comandos import *


class ClienteUnoR4Wifi(Cliente):
    '''
        Descrição dos atributos

    '''

    def __init__(self, porta_cliente: int, porta_robo: int):
        super().__init__(porta_cliente, porta_robo)
        self._T1 = 0
        self._T2 = 0
        self._estado = 1
        self.valor = 0

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
        try:
            self._socket.close()
        except:
            pass
        print("Conexão com Servidor Finalizada")

    def enviar_mensagem(self, mensagem:str):
        self._socket.sendall((mensagem).encode())
    
    def receber_mensagem(self):
        self._resposta = self._socket.recv(1024)
    

    def escutar_servidor(self):
        buffer = b''  # buffer acumulativo

        while self._estado:
            try:
                self.receber_mensagem()

                if not self._resposta:
                    continue
                buffer += self._resposta

                current_line = readline.get_line_buffer()
                sys.stdout.write('\r' + ' ' * (len(current_line)+30) + '\r')

                # Processa floats binários completos (4 bytes)
                while len(buffer) >= 4:
                    chunk = buffer[:4]
                    buffer = buffer[4:]
                    valor_float = struct.unpack('f', chunk)[0]
                    
                    if valor_float != 1:
                        self.valor = valor_float
                        print(f"[Robô]: {self.valor:.2f}")

                sys.stdout.write(f"Comando: {current_line}")
                sys.stdout.flush()

            except socket.timeout:
                continue
            except OSError:
                break

    def escutar_cliente(self):
        while self._estado:
            comando = input()
            if comando.lower() == "sair":
                self.enviar_mensagem("ER")
                time.sleep(0.5)
                self._estado = 0
                break
            else:
                self.enviar_mensagem(comando)


            

    def get_valor(self):
        return self.valor
        
    def get_resposta(self):
        return self._resposta

    def iniciar_threads(self):
        thread = threading.Thread(target=self.escutar_servidor, daemon=True)
        thread.start()
        thread1 = threading.Thread(target=self.escutar_cliente, daemon=True)
        thread1.start()


    def solicitar_status(self):
        print("status\n")
    
    def alterar_conexao(self):
        print("conexao\n")

    def testar_tempo_conexao(self, mensagem):
        print("tempo\n")

    def metodos(self):
        global enviar, receber, esperar
        enviar = self.enviar_mensagem
        receber = self.get_valor
        esperar = time.sleep

    def setup(self) -> None:
        while (True):
            comando = input()
            if comando.lower() == "*":
                self.enviar_mensagem(comando)
                break
            self.enviar_mensagem(comando)

    def executar(self):
        
        self.descoberta()
        self.conectar()
        self.metodos()
        self.iniciar_threads()
        self.setup()

    
        while self._estado:

            self.acao()

        self.desconectar()
    
    def acao(self):
        '''
        
            Descrição dos metodos enviar, esperar, receber, etc
            achei melhor deixar assim do que self.metodo

        '''

        enviar(SENSOR_ULTRASSONICO)
        enviar(velociade(100,100))

        if(receber() < 15):
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_TRAZ)
            esperar(0.5)
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_DIREITA)
            esperar(0.5)
        
        
        enviar(MOVER_PARA_FRENTE)

        esperar(0.05)


def velociade( a, b):
    return "VS/" + str(a) + "/" + str(b)
        
        
        

# Execução de um exemplo de troca de mensagens entre cliente e servidor
if __name__ == "__main__":
    
    PORTA_CLIENTE = 5005
    PORTA_ROBO = 4210

    cliente = ClienteUnoR4Wifi(PORTA_CLIENTE, PORTA_ROBO)

    cliente.executar()

