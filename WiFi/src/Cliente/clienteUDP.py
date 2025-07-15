import socket
import threading
import readline 
import sys
import time

ROBOT_PORT = 4210        
MY_PORT = 5005

T1 = 0  
T2 = 0  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", MY_PORT)) 
sock.settimeout(2.0)

mensagem = b"WeMosD1"
sock.sendto(mensagem, ("255.255.255.255", ROBOT_PORT))

try:
    data, addr = sock.recvfrom(1024)
    ROBOT_IP = addr[0]
    print(f"Robot IP: {ROBOT_IP}")
except socket.timeout:
    print("ANR")
    sock.close()
    sys.exit()

def escutar_robo():
    global T2, T1
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            T2 = time.perf_counter()  # pega tempo preciso ao receber
            rtt = (T2 - T1) * 1000  # em milissegundos

            current_line = readline.get_line_buffer()
            sys.stdout.write('\r' + ' ' * (len(current_line)+20) + '\r')
            print(f"[Robô]: {data.decode()} | {rtt:.2f} ms")
            sys.stdout.write(f"Comando: {current_line}")
            sys.stdout.flush()
        except socket.timeout:
            continue
        except OSError:
            break  

thread = threading.Thread(target=escutar_robo, daemon=True)
thread.start()

print("Cliente UDP iniciado. Digite comandos para o robô.")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input()
    if comando.lower() == "sair":
        break
    T1 = time.perf_counter()  # marca tempo de envio
    sock.sendto(comando.encode(), (ROBOT_IP, ROBOT_PORT))

sock.close()
print("Encerrando...")
