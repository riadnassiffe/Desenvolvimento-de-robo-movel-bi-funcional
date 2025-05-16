#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "SUA_REDE";
const char* password = "SUA_SENHA";

WiFiUDP udp;
unsigned int localPort = 4210;  // Porta onde o robô escuta
char incomingPacket[255];

IPAddress pcIP(192, 168, 0, 123); // IP do seu PC
unsigned int pcPort = 5005;       // Porta que o Python está escutando

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("WiFi conectado");

  udp.begin(localPort);
  Serial.printf("Escutando na porta UDP %d\n", localPort);
}

void loop() {
  // RECEBER comandos do PC
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = '\0';
    }
    Serial.printf("Recebido: %s\n", incomingPacket);

    // ENVIA resposta para o PC
    udp.beginPacket(udp.remoteIP(), udp.remotePort());  // responde ao remetente
    udp.print("Confirmado: ");
    udp.print(incomingPacket);
    udp.endPacket();
  }

  delay(10);
}
