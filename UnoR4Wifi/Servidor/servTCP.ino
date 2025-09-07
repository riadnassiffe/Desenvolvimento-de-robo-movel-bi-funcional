#include <WiFiS3.h>
#include <WiFiUdp.h>

const int PinTrigger = 2;
const int PinEcho = 3;

long duration;
float distance;

char ssid[] = "ZTE_2.4G_7NXk26";
char pass[] = "TUfyZZFT";

WiFiUDP udp;
unsigned int localPort = 4210;
char incomingPacket[255];
bool pcConectado = false;
IPAddress pcIP;
unsigned int pcPort;

WiFiServer server(4210);
WiFiClient client;

int LED = LED_BUILTIN;
bool estadoLED = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

  pinMode(PinTrigger, OUTPUT);
  pinMode(PinEcho, INPUT);

  Serial.print("Conectando ao WiFi");
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado!");
  Serial.print("IP do UNO R4 WiFi: ");
  Serial.println(WiFi.localIP());

  udp.begin(localPort);
  server.begin();

  Serial.println("UDP e TCP escutando na porta 4210...");
}

void loop() {
  // --- Descoberta via UDP ---
  while (!pcConectado) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
      int len = udp.read(incomingPacket, 254);
      incomingPacket[len] = '\0';
      Serial.print("Recebido (descoberta): ");
      Serial.println(incomingPacket);


      if (strcmp(incomingPacket, "WeMosD1") == 0) {
        pcIP = udp.remoteIP();
        pcPort = udp.remotePort();
        pcConectado = true;

        udp.beginPacket(pcIP, pcPort);
        udp.print("UNO R4 WiFi aqui!");
        udp.endPacket();

        Serial.println("Resposta UDP enviada.");
      }
    }
  }

  // --- Conexão TCP ---
  while (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("Cliente TCP conectado.");
    }
  }

  // --- Verifica WiFi ---
  if (WiFi.status() != WL_CONNECTED) {
    WiFi.disconnect();
    WiFi.begin(ssid, pass);
  }


  // --- Recebe comando TCP ---
  if (client.available()) {
    String comando = client.readStringUntil('\n');
    comando.trim();
    Serial.print("Recebido: ");
    Serial.println(comando);

    if (comando == "1") {
      digitalWrite(LED, LOW);
      estadoLED = true;
    } else if (comando == "0") {
      digitalWrite(LED, HIGH);
      estadoLED = false;
    }

    client.print("Comando recebido: " + comando);
  }

  delay(5);
}


