from robo import *
import sys

def setup():
    enviar("M/8/9/10/11/12/13")
    esperar(0.5)
    enviar("U/6/7")
    esperar(0.5)
    enviar("*")
    

try:
    conectar_robo()
    setup()

    enviar(velocidade(120, 120))
    
    while True:
        
        enviar(SENSOR_ULTRASSONICO)
        valor = receber()
        print(valor)

        if(valor < 20):
            print("parou")
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
        
except KeyboardInterrupt:
    print("\nLoop interrompido pelo usuário.")
except Exception as e:
    print(f"Erro fatal durante o loop: {e}")
finally:
    desconectar_robo()
    print("Programa finalizado.")