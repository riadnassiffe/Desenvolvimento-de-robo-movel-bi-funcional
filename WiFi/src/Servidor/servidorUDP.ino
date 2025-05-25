#include <ESP8266WiFi.h>
#include <WiFiUdp.h>


const int PinTrigger = D1; 
const int PinEcho = D2;    

long duration;
float distance;

const char* ssid = "ZTE_2.4G_7NXk26";
const char* password = "TUfyZZFT";

WiFiUDP udp;
unsigned int localPort = 4210;
char incomingPacket[255];

int LED = LED_BUILTIN;
bool estadoLED = false;


IPAddress pcIP(192, 168, 1, 8);
unsigned int pcPort = 5005;  

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

  if (WiFi.status() != WL_CONNECTED) {
    WiFi.reconnect();
  }
  /*
  digitalWrite(PinTrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(PinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(PinTrigger, LOW);

  duration = pulseIn(PinEcho, HIGH, 30000);
  if (duration == 0) {
    distance = 0;
  } else {
    distance = (duration * 0.0343) / 2;
  }

  if (distance > 20) { 
    //digitalWrite(LED_BUILTIN, HIGH);

  } else { 
    //digitalWrite(LED_BUILTIN, LOW);
  }
  char distStr[16];
  dtostrf(distance, 6, 2, distStr);
  udp.beginPacket(pcIP, pcPort);
  udp.print(distStr);
  udp.endPacket();
  */
  int packetSize = udp.parsePacket();
  if (packetSize) {

    udp.beginPacket(pcIP, pcPort);
    udp.printf("Comando recebido: %s | LED está %s", incomingPacket, estadoLED ? "LIGADO" : "DESLIGADO");
    udp.endPacket();

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

  }

  delay(5);
}