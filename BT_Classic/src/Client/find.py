# Identificar o Dispositivo
import asyncio
from bleak import BleakScanner, BleakClient

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"\nDispositivo encontrado: {d.name} - {d.address}")
        try:
            async with BleakClient(d.address) as client:
                if client.is_connected:
                    services = client.services 
                    for service in services:
                        print(f"  Serviço: {service.uuid} - {service.description}")
                        for char in service.characteristics:
                            print(f"    CHAR_UUID: {char.uuid} - {char.description} - Propriedades: {char.properties}")
        except Exception as e:
            print(f"  Não foi possível conectar ao dispositivo: {e}")

asyncio.run(run())
