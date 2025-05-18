import socket
import threading
import readline  # Para manipular input sem bagunçar
import sys

ROBOT_IP = "192.168.1.11"  # IP do ESP
ROBOT_PORT = 4210          # Porta do robô
MY_PORT = 5005             # Porta do PC (onde escuta respostas)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", MY_PORT))  # Escuta nesta porta
sock.settimeout(2.0)  # Tempo limite para resposta

def escutar_robo():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # Salva o que o usuário está digitando no momento
            current_line = readline.get_line_buffer()
            sys.stdout.write('\r' + ' ' * (len(current_line)+10) + '\r')  # Limpa linha
            print(f"[Robô]: {data.decode()}")
            sys.stdout.write(f"Comando: {current_line}")
            sys.stdout.flush()
        except socket.timeout:
            continue
        except OSError:
            break  # Socket fechado

thread = threading.Thread(target=escutar_robo, daemon=True)
thread.start()

print("Cliente UDP iniciado. Digite comandos para o robô.")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input()

    if comando.lower() == "sair":
        break

    # Envia comando para o robô
    sock.sendto(comando.encode(), (ROBOT_IP, ROBOT_PORT))


sock.close()
print("Encerrando...")
