import socket
import threading
import readline 
import sys
import time

ROBOT_IP = "192.168.1.2"  
ROBOT_PORT = 4210        
MY_PORT = 5005           

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", MY_PORT)) 
sock.settimeout(2.0)  

def escutar_robo():
    while True:
        try:
            data = sock.recvfrom(1024)
            t2 = time.time()
            rtt = (t2 - t1)
            current_line = readline.get_line_buffer()
            sys.stdout.write('\r' + ' ' * (len(current_line)+10) + '\r')  # Limpa linha
            print(f"[Robô]: {data.decode()} | RTT: {rtt:.2f} ms")
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
    t1 = time.time()
    if comando.lower() == "sair":
        break
    sock.sendto(comando.encode(), (ROBOT_IP, ROBOT_PORT))

    


sock.close()
print("Encerrando...")
