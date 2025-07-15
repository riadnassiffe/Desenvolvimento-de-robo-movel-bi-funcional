import socket
import threading
import readline
import sys
import time

ROBOT_PORT = 4210
MY_PORT = 5005   

T1 = 0  
T2 = 0  

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_sock.bind(("", MY_PORT))
udp_sock.settimeout(2.0)

mensagem = b"WeMosD1"
udp_sock.sendto(mensagem, ("255.255.255.255", ROBOT_PORT))

try:
    data, addr = udp_sock.recvfrom(1024)
    ROBOT_IP = addr[0]
    print(f"Robô respondeu via UDP: {data.decode()}")
    print(f"Endereço do robô: {ROBOT_IP}")
except socket.timeout:
    print("Robô não respondeu à descoberta (UDP).")
    udp_sock.close()
    sys.exit()

udp_sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((ROBOT_IP, ROBOT_PORT))
except socket.error as e:
    print(f"Erro ao conectar via TCP: {e}")
    sys.exit()

sock.settimeout(2.0)

def escutar_robo():
    global T2, T1
    while True:
        try:
            data = sock.recv(1024)
            T2 = time.perf_counter()
            rtt = (T2 - T1) * 1000  # milissegundos

            current_line = readline.get_line_buffer()
            sys.stdout.write('\r' + ' ' * (len(current_line)+30) + '\r')
            print(f"[Robô]: {data.decode()} | RTT: {rtt:.2f} ms")
            sys.stdout.write(f"Comando: {current_line}")
            sys.stdout.flush()
        except socket.timeout:
            continue
        except OSError:
            break

thread = threading.Thread(target=escutar_robo, daemon=True)
thread.start()

print("\nCliente TCP iniciado. Digite comandos para o robô.")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input()
    if comando.lower() == "sair":
        break
    T1 = time.perf_counter()
    sock.sendall((comando+'\n').encode())

sock.close()
print("Encerrando...")
