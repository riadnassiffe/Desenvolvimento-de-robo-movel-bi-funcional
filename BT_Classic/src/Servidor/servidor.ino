#include <SoftwareSerial.h>

SoftwareSerial BTSerial(D6, D7); // RX, TX (Bluetooth)
const int ledPin = D4; // LED interno do Wemos (GPIO2)

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); // Começa desligado

  Serial.begin(9600);         // Monitor Serial
  BTSerial.begin(9600);       // Comunicação Bluetooth
  Serial.println("Pronto para comunicação via Bluetooth!");
}

void loop() {
  // Recebendo comando via Bluetooth (do PC)
  if (BTSerial.available()) {
    String comando = BTSerial.readStringUntil('\n');
    Serial.println("Mensagem recebida do PC: " + comando);
    
    if (comando == "0") {
      digitalWrite(ledPin, HIGH);
    } else if (comando == "1") {
      digitalWrite(ledPin, LOW);
    } else {
      BTSerial.println("Comando desconhecido: " + comando);
    }
    
  }

  // Enviando mensagem digitada no Monitor Serial (para o PC)
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    BTSerial.println("Mensagem do Wemos: " + comando);
  }
}
