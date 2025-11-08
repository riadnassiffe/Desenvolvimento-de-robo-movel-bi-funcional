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
    enviar("M/8/9/10/11/12/13")
    esperar(0.5)
    enviar("U/6/7")
    esperar(0.5)
    enviar("*") # Obrigatório para finalizar a configuração

'''
--- Loop ---
Crie a logica da ação do robo
ou seja, envie mensagens (ordens)
e receba o resultado delas
'''

def loop():
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
        esperar(0.4)
        enviar(MOTOR_PARAR)
        esperar(0.5)
    else:

        enviar(MOVER_PARA_FRENTE)

    esperar(0.05) #delay do loop

def main():
    
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
    """Formata o comando de velocidade."""
    return "VS/" + str(a) + "/" + str(b)