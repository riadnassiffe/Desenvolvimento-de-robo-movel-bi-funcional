#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// Definição dos pinos para o sensor ultrassônico no Wemos D1 R2
const int PinTrigger = D1; // GPIO5
const int PinEcho = D2;    // GPIO4
// Variáveis para cálculo da distância
long duration;
float distance;

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
  pinMode(PinTrigger, OUTPUT);
  pinMode(PinEcho, INPUT);

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
  // Dispara pulso
  digitalWrite(PinTrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(PinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(PinTrigger, LOW);

  duration = pulseIn(PinEcho, HIGH, 30000);
  distance = (duration * 0.0343) / 2;

  // Verifica a distância e toma ações
  if (distance > 20) { // Se a distância for maior que 0.2 metros
    digitalWrite(LED_BUILTIN, HIGH); // Liga o LED

  } else { // Se a distância for menor ou igual a 0.2 metros
    digitalWrite(LED_BUILTIN, LOW); // Desliga o LED
  }
  char distStr[16];
  dtostrf(distance, 6, 2, distStr);
  udp.beginPacket(pcIP, pcPort);
  udp.print(distStr);
  udp.endPacket();

  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 254);
    incomingPacket[len] = '\0';

    Serial.printf("Recebido: %s\n", incomingPacket);

    if (strcmp(incomingPacket, "1") == 0) {
      digitalWrite(LED, LOW);
      estadoLED = true;
    } else if (strcmp(incomingPacket, "0") == 0) {
      digitalWrite(LED, HIGH);
      estadoLED = false;
    }

    udp.beginPacket(pcIP, pcPort);
    udp.printf("Comando recebido: %s | LED está %s", incomingPacket, estadoLED ? "LIGADO" : "DESLIGADO");
    udp.endPacket();
  }

  delay(10);
}

/*
Resolver isso
--------------- CUT HERE FOR EXCEPTION DECODER ---------------

 ets Jan  8 2013,rst cause:4, boot mode:(3,6)

wdt reset
load 0x4010f000, len 3424, room 16 
tail 0
chksum 0x2e
load 0x3fff20b8, len 40, room 8 
tail 0
chksum 0x2b
csum 0x2b
v00043be0 
~ld
��n�r��n|�l�l`bbrl�nb�nl`�rl�l��Conectando ao WiFi..............
WiFi conectado
IP do ESP8266: 192.168.1.11
Escutando UDP na porta 4210

 ets Jan  8 2013,rst cause:4, boot mode:(3,6)

wdt reset
load 0x4010f000, len 3424, room 16 
tail 0
chksum 0x2e
load 0x3fff20b8, len 40, room 8 
tail 0
chksum 0x2b
csum 0x2b
v00043be0
~ld
��n�r��n|�l�l`bbrl�nb�nl`�rl�l��Conectando ao WiFi..............
WiFi conectado
IP do ESP8266: 192.168.1.11
Escutando UDP na porta 4210
*/