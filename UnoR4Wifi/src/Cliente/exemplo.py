"""
Script principal para controle de um robô via comunicação.

Este script define a lógica de operação do robô, incluindo a configuração
inicial (setup) e o loop de comportamento principal (loop). 
"""
from clienteUnoR4WiFi import ClienteUnoR4Wifi
from robo import *
import sys
from comandos import *
import time

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
    # Exemplo: Configura o pino do buzzer.
    enviar(CONFIGURAR_BUZZER + "/7")
    esperar(0.5)
    # Envia o comando para o robô sair do modo de configuração e entrar no loop de ação.
    enviar(SETUP_CONCLUIDO)

'''
--- Loop ---
Crie a logica da ação do robo
ou seja, envie mensagens (ordens)
e receba o resultado delas
'''

def loop():
    
    # Enviando comando para ativar o buzzer
    enviar(BUZZER_ATIVAR_DELAY + "500/100")
    # Pequena pausa para controlar a frequência do loop.
    esperar(2)

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
        # 1. Conecta ao robô, passando a classe de cliente específica.
        conectar_robo(ClienteUnoR4Wifi)
        # 2. Executa a configuração inicial.
        setup()
        print("Iniciando loop de ação. Pressione Ctrl+C para parar.")
                
        # 3. Entra no loop infinito de controle.
        while True:
           loop()
            
    except KeyboardInterrupt:
        # Permite que o usuário pare o script com Ctrl+C.
        print("\nLoop interrompido pelo usuário.")
    except Exception as e:
        # Captura outros erros que podem ocorrer (ex: erros de comunicação).
        print(f"Erro fatal durante o loop: {e}")
    finally:
        # 4. Garante que a desconexão seja sempre chamada, mesmo se ocorrer um erro.
        desconectar_robo()
        print("Programa finalizado.")

if __name__ == "__main__":
    main()

