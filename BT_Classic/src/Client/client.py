import asyncio
from bleak import BleakClient

# UUID da característica (substitua pelo correto)
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data):
    print(f"Recebido via notificação: {data.decode()}")

async def main():
    address = "3C:A5:49:DE:91:9B"  # Endereço MAC do JDY-18
    async with BleakClient(address) as client:
        print("Tentando conectar ao JDY-18...")

        # Verificar se a conexão foi bem-sucedida
        if not client.is_connected:
            print("Não foi possível conectar ao JDY-18.")
            return

        print("Conectado com sucesso!")

        # Inscrever-se para notificações
        await client.start_notify(CHAR_UUID, notification_handler)

        while True:
            msg = input("Digite algo para enviar ao Wemos (ou 'sair' para encerrar): ")
            if msg.lower() == 'sair':
                break

            # Enviar a mensagem para o Wemos
            await client.write_gatt_char(CHAR_UUID, msg.encode())

        await client.stop_notify(CHAR_UUID)
        print("Notificações paradas. Conexão encerrada.")

# Executar a função principal
asyncio.run(main())
