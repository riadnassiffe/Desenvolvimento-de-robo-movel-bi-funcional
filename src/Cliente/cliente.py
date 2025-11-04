'''
    Cliente

    Código que implementa a Classe cliente responsável por comunicar-se
    com o dispositivo executando o servidor em um Arduíno Uno. Utilize
    essa classe para conectar-se e trocar mensagens via blueetooth com
    o robô.
'''

import bluetooth
import struct
from time import time
from erro import *

class Cliente:
    '''
        Descrição dos atributos
    
        addr: Uma string que representa o endereço do módulo Bluetooth HC-05 utilizado no robô para 
        efetuar a comunicação.
      
        Porta: Número inteiro que identifica a porta do computador que será utilizada para realizar
        a comunicação com o servidor.
      
        socket: Objeto do tipo BluetoothSocket (disponibilizado através da biblioteca PyBluez)
        configurado para usar o protocolo de comunicação Bluetooth RFCOMM. Esse objeto é utilizado
        para realizar chamadas aos métodos responsáveis pela troca de mensagem propriamente dita
        entre os dispositivos Bluetooth do dispositivo cliente e do dispositivo servidor.
    '''

    def __init__(self, addr:str, porta:int):
        self.addr = addr
        self.porta = porta
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def conectar(self):
        '''
            Tenta conectar o socket Bluetooth ao dispositivo cujo endereço corresponde ao armazenado 
            no atributo addr. Em caso de falha, um erro indicando que não foi possível estabelecer a
            comunicação é disparado.
        '''
        try:
            self.socket.connect((self.addr, self.porta))
        except:
            raise ErroConexaoInexistente()

    def desconectar(self) -> None:
        '''
            Envia o comando específico para encerrar a comunicação entre cliente e servidor,
            fechando o sockect utilizado para o envio de mensagens após conclusão.
        '''
        self.enviar_mensagem("ER")
        self.socket.close()

    def enviar_mensagem(self, mensagem:str) -> None:
        '''
            Envia uma string recebida pelo parâmetro mensagem para o dispositivo conectado através
            do método conectar. Atenção, é necessário que exista uma conexão ativa para que esse
            método funcione. Utilize esse método para enviar os comandos para o servidor definidos
            nessa documentação em seção posterior.

            Parâmetros:
                mensagem - str - string que será enviada para o servidor
        '''
        self.socket.sendall(mensagem)

    def get_resposta(self) -> float:
        '''
            Retorna a saída recebida do servidor após a execução de um comando. Caso nenhum comando
            tenha sido enviado previamente, o cliente ficará aguardando uma resposta, uma vez que a
            comunicação com o servidor é configurada como síncrona.

            Retorno:
                saida - float - dado recebido do servidor após execução de um comando
        '''

        # Armazena os bytes recebidos do servidor
        recebido = b''
        
        # Recebe quatro bytes do servidor (tamanho padrão de todo retorno),
        # sendo um byte recebido a cada iteração do laço
        for i in range(4):
            recebido += self.socket.recv(1)

        # Converte os bytes para o formato float
        saida = struct.unpack('f', recebido)[0]

        # Verifica se a saida corresponde a um código de erro.
        # Se sim, dispara o devido erro conforme definição.
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

# Execução de um exemplo de troca de mensagens entre cliente e servidor
if __name__ == "__main__":
    
    # Criando um objeto cliente
    # Observe que o endereço utilizado corressponde ao endereço do dispositivo
    # bluetooth conectado ao Arduíno Uno. Esse valor é diferente para outros
    # dispositivos, sendo assim, caso queira testar esse código altere o valor
    # do endereço abaixo para corresponder com o de seu dispositivo conectado
    # ao servidor.
    cliente = Cliente("98:d3:31:fc:50:4c", 1)
    # Realizando a conexão com o servidor
    cliente.conectar()

    while True:

        print("-"*25)
        
        print("Para sair pressione apenas Enter...")
        
        # Recebendo um comando para enviar ao servidor
        comando = input("Digite o Comando: ")
        
        # String utilizada para interromper a execução desse exemplo de código
        if comando == "":
            # Encerrando a comunicação entre cliente e servidor
            cliente.desconectar()
            break

        print("-"*25)
        
        # Enviando o comando ao servidor
        cliente.enviar_mensagem(comando)

        # Exibindo o retorno recebido do comando enviado anteriormente
        print(cliente.get_resposta())