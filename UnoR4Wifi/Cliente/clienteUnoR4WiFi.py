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
    --- Print -----

    essa mudança é apenas para que ao imprimir um valor,e ao inserir um valor
    fique mais agradavel no terminal

'''
builtins._orig_print = print

def safe_prompt(label="Comando: "):
    sys.stdout.write(label)
    sys.stdout.flush()

def safe_print(msg: str):
    current = readline.get_line_buffer()
    sys.stdout.write('\r' + ' ' * (len(current) + 12) + '\r')
    sys.stdout.flush()

    builtins._orig_print(msg)

    sys.stdout.write(current)
    sys.stdout.flush()
    
def patched_print(*args, **kwargs):
    safe_print(" ".join(str(a) for a in args))

builtins.print = patched_print

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

    def escutar_cliente(self):
        while self._estado:
            comando = input()
            if comando.lower() == "sair":
                self.enviar_mensagem("ER")
                time.sleep(0.5)
                self._estado = 0
                self.valor = 0
                break
            else:
                self.enviar_mensagem(comando)

    def iniciar_threads(self, n):

        match n:
            case(0):
                thread = threading.Thread(target=self.escutar_servidor, daemon=True)
                thread.start()
            case(1):
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
        receber = self.receber_mensagem
        esperar = time.sleep

    def setup(self) -> None:
        while (True):
            safe_prompt()
            comando = input()
            self.enviar_mensagem(comando)
            if comando.lower() == "*":   
                break
             
    def executar(self):
        
        self.descoberta()
        self.conectar()
        self.metodos()
        self.iniciar_threads(0)
        self.setup()
        self.iniciar_threads(1)
    
        while self._estado:

            self.acao()

        self.desconectar()
    
    def acao(self):

        enviar(velocidade(120,120))

        enviar(SENSOR_ULTRASSONICO)
        valor = receber()
        print(f"distancia: {valor:.2f}")

        if(valor < 20):
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_TRAZ)
            esperar(0.5)
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_DIREITA)
            esperar(0.4)
            enviar(MOTOR_PARAR)
            esperar(0.5)
            
        enviar(MOVER_PARA_FRENTE)

        esperar(0.05)
    
def velocidade( a, b):
    return "VS/" + str(a) + "/" + str(b)
        
# Execução de um exemplo de troca de mensagens entre cliente e servidor
if __name__ == "__main__":
    
    PORTA_CLIENTE = 5005
    PORTA_ROBO = 4210

    cliente = ClienteUnoR4Wifi(PORTA_CLIENTE, PORTA_ROBO)
    #cliente.robo = 

    cliente.executar()

'''
        enviar(velocidade(120,120))

        enviar(SENSOR_ULTRASSONICO)
        valor = receber()
        print(f"distancia: {valor:.2f}")

        if(valor < 20):
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_TRAZ)
            esperar(0.5)
            enviar(MOTOR_PARAR)
            esperar(0.5)
            enviar(MOVER_PARA_DIREITA)
            esperar(0.4)
            enviar(MOTOR_PARAR)
            esperar(0.5)
            
        enviar(MOVER_PARA_FRENTE)

        esperar(0.05)

        
        self.enviar_mensagem("VS/120/120")

        self.enviar_mensagem("RU")
        valor = self.receber_mensagem()
        print(f"distancia: {valor:.2f}")

        if(valor < 15):
            self.enviar_mensagem("MP")
            time.sleep(0.5)

            self.enviar_mensagem("MD")
            time.sleep(0.3)

            self.enviar_mensagem("MP")
            time.sleep(0.5)
            
        self.enviar_mensagem("MF")
        
        time.sleep(0.05)

'''