#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "ZTE_2.4G_7NXk26";       // substitua pelo nome da sua rede WiFi
const char* password = "TUfyZZFT";  // substitua pela senha da sua rede WiFi

WiFiUDP udp;
unsigned int localPort = 4210;  // Porta onde o robô escuta
char incomingPacket[255];

int LED = LED_BUILTIN;
bool estadoLED = false; // Estado atual do LED

// IP do seu PC — ajuste para o IP correto da sua máquina
IPAddress pcIP(192, 168, 1, 8);
unsigned int pcPort = 5005;  // Porta que o Python está escutando

void setup() {
  Serial.begin(115200);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH); // Apaga o LED (ativo em LOW no ESP8266)

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  Serial.print("IP do ESP8266: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  Serial.printf("Escutando UDP na porta %d\n", localPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = '\0';
    }

    Serial.printf("Recebido: %s\n", incomingPacket);

    String comando = String(incomingPacket);
    if (comando == "1") {
      digitalWrite(LED, LOW);  // Liga LED (ativo em LOW)
      estadoLED = true;
    } else if (comando == "0") {
      digitalWrite(LED, HIGH); // Desliga LED
      estadoLED = false;
    }

    // Envia a resposta explicitamente para o IP e porta do PC
    udp.beginPacket(pcIP, pcPort);
    udp.print("Comando recebido: ");
    udp.print(comando);
    udp.print(" | LED está ");
    udp.print(estadoLED ? "LIGADO" : "DESLIGADO");
    udp.endPacket();
  }

  delay(10);
}
