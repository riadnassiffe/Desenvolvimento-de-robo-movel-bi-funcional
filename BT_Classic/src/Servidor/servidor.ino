#include <SoftwareSerial.h>

SoftwareSerial BTSerial(D6, D7); 
const int ledPin = D4; 

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH); 

  Serial.begin(9600);         
  BTSerial.begin(9600);       
  Serial.println("Pronto para comunicação via Bluetooth!");
}

void loop() {
  
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

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    BTSerial.println("Mensagem do Wemos: " + comando);
  }
}
