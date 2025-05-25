#include <ESP8266WiFi.h>
#include <WiFiClient.h>

const char* ssid = "ZTE_2.4G_7NXk26";
const char* password = "TUfyZZFT";

WiFiServer server(4210);

int LED = LED_BUILTIN;
bool estadoLED = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  Serial.print("IP do ESP8266: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("Servidor TCP iniciado.");
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Cliente conectado.");
    while (client.connected()) {
      if (client.available()) {
        String comando = client.readStringUntil('\n');
        comando.trim();
        Serial.println("Recebido: " + comando);

        if (comando == "1") {
          digitalWrite(LED, LOW);
          estadoLED = true;
        } else if (comando == "0") {
          digitalWrite(LED, HIGH);
          estadoLED = false;
        }

        String resposta = "Comando recebido: " + comando;
        resposta += " | LED está ";
        resposta += (estadoLED ? "LIGADO" : "DESLIGADO");
        resposta += "\n";

        client.print(resposta);
      }
    }
    client.stop();
    Serial.println("Cliente desconectado.");
  }
}
