import socket
import threading
import readline
import sys
import time

ROBOT_IP = "192.168.1.2"   
ROBOT_PORT = 4210          

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ROBOT_IP, ROBOT_PORT))
sock.settimeout(2.0)

def escutar_robo():
    while True:
        try:
            data = sock.recv(1024)
            t2 = time.time()
            rtt = (t2 - t1) * 1000  # em milissegundos
            current_line = readline.get_line_buffer()
            sys.stdout.write('\r' + ' ' * (len(current_line) + 20) + '\r')
            print(f"[Robô]: {data.decode()} | RTT: {rtt:.2f} ms")
            sys.stdout.write(f"Comando: {current_line}")
            sys.stdout.flush()
        except socket.timeout:
            continue
        except OSError:
            break

thread = threading.Thread(target=escutar_robo, daemon=True)
thread.start()

print("Cliente TCP iniciado. Digite comandos para o robô.")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input()
    t1 = time.time()
    if comando.lower() == "sair":
        break
    sock.sendall(comando.encode())

sock.close()
print("Encerrando...")
