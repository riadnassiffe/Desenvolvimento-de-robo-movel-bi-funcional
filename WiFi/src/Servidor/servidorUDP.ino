#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const int PinTrigger = D1; 
const int PinEcho = D2;    

long duration;
float distance;

const char* ssid = "CLARO_2GDF6584";
const char* password = "12DF6584";//TUfyZZFT

WiFiUDP udp;
unsigned int localPort = 4210;
unsigned int pcPort;
bool pcConectado = false;  
IPAddress pcIP;
char incomingPacket[255];

int LED = LED_BUILTIN;
bool estadoLED = false;


void setup() {
  Serial.begin(115200);

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH); 
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

  while (!pcConectado) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
      int len = udp.read(incomingPacket, 254);
      incomingPacket[len] = '\0';
      Serial.printf("Recebido (descoberta): %s\n", incomingPacket);

      if (strcmp(incomingPacket, "WeMosD1") == 0) {
        pcIP = udp.remoteIP();
        pcPort = udp.remotePort();
        pcConectado = true;

        udp.beginPacket(pcIP, pcPort);
        udp.print("ESP8266 aqui!");
        udp.endPacket();

        Serial.println("Cliente conectado!");
      }
    }
  }

  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
  }
    
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
    udp.printf("Comando recebido: %s", incomingPacket);
    udp.endPacket();

  }

  delay(5);
}

