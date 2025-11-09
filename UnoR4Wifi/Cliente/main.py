"""
Script principal para controle de um robô via comunicação.

Este script define a lógica de operação do robô, incluindo a configuração
inicial (setup) e o loop de comportamento principal (loop). 
"""

from robo import *
import sys
from comandos import *
import time

'''
--- Setup ---
Informe o robo a configuração dele
lembre de finalizar enviando "*"
'''

def setup():
    """
    Local onde o usuário deve inseria a configuração dos pinos e componentes iniciais do robô.

    Finalize enviando o comando 'SETUP_CONCLUIDO'
    para sinalizar que o robô está pronto para iniciar o loop principal.
    """
    enviar(CONFIGURAR_MOTORES + "/8/9/10/11/12/13")
    esperar(0.5)
    enviar(CONFIGURAR_ULTRASSONICO + "/6/7")
    esperar(0.5)
    enviar(SETUP_CONCLUIDO) # Obrigatório para finalizar a configuração

'''
--- Loop ---
Crie a logica da ação do robo
ou seja, envie mensagens (ordens)
e receba o resultado delas
'''

def loop():
    """
    Executa o ciclo da lógica de controle do robô o qual deve
    ser criado pelo usuário.
    """
    enviar(velocidade(120, 120))
    enviar(SENSOR_ULTRASSONICO)
    valor = receber()
    print(valor)

    if (valor < 20):
        enviar(MOTOR_PARAR)
        esperar(0.5)
        enviar(MOVER_PARA_TRAZ)
        esperar(0.5)
        enviar(MOTOR_PARAR)
        esperar(0.5)
        enviar(MOVER_PARA_DIREITA)
        esperar(0.5)
        enviar(MOTOR_PARAR)
        esperar(0.5)
    else:
        enviar(MOVER_PARA_FRENTE)

    esperar(0.05)

def main():
    """Função principal que gerencia o ciclo de vida da execução do robô.

    Estabelece a conexão, executa a configuração (setup) e, em seguida,
    entra no loop de ação principal (loop), que é executado continuamente.
    
    Captura 'KeyboardInterrupt' (Ctrl+C) para permitir uma interrupção
    limpa, garantindo que o robô seja desconectado corretamente.
    Trata também outras exceções que possam ocorrer durante a execução,
    tais exeções fazem parte da classe Erros.
    """
    
    try:
        conectar_robo()
        setup()
        print("Iniciando loop de ação. Pressione Ctrl+C para parar.")
                
        while True:
           loop()
            
    except KeyboardInterrupt:
        print("\nLoop interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro fatal durante o loop: {e}")
    finally:
        desconectar_robo()
        print("Programa finalizado.")

if __name__ == "__main__":
    main()

'''
 --- Funções De Ajuda ---
 opcional, isso depende caso o usuário precise
 apenas um exemplo para facilitar o uso de enviar
 comandos para alterar a velocidade do robo
'''
def velocidade(a, b):
    """Formata o comando de velocidade para os motores.

    Cria uma string de comando padronizada "VS/a/b" que pode ser
    enviada ao robô para definir a velocidade dos motores.

    Args:
        a (int): A velocidade desejada para o motor A (ou esquerdo).
        b (int): A velocidade desejada para o motor B (ou direito).

    Returns:
        str: A string de comando formatada (ex: "VS/120/120").
    """
    return "VS/" + str(a) + "/" + str(b)