import socket

ROBOT_IP = "192.168.1.11"  # IP do ESP
ROBOT_PORT = 4210          # Porta do robô
MY_PORT = 5005             # Porta do PC (onde escuta respostas)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", MY_PORT))  # Escuta nesta porta

sock.settimeout(2.0)  # Tempo limite para resposta

print("Cliente UDP iniciado. Digite comandos para o robô.")
print("Digite 'sair' para encerrar.\n")

while True:
    comando = input("Comando: ")

    if comando.lower() == "sair":
        break

    # Envia comando para o robô
    sock.sendto(comando.encode(), (ROBOT_IP, ROBOT_PORT))

    try:
        # Espera resposta do robô
        data, addr = sock.recvfrom(1024)
        print("Resposta do robô:", data.decode())
    except socket.timeout:
        print("Sem resposta do robô.")

sock.close()
