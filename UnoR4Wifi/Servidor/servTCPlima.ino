#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <Wire.h>

//Variaves para que se possa estabelecer uma conexção entre o servidor e cliente, um broadcast para encontrar o cliente via UDP, depois mantem conexção TCP
int teste = 0;
char ssid[] = "kadu"; //" kadu  ZTE_2.4G_7NXk26";
char pass[] = "12345678"; //"TUfyZZFT 12345678";

WiFiUDP udp;
unsigned int localPort = 4210;
char incomingPacket[255];
bool pcConectado = false;
IPAddress pcIP;
unsigned int pcPort;

WiFiServer server(4210);
WiFiClient client;

// Definição da estrutura de dados utilizada para representação de informações que são envidas
// e recebidas na comunicação entre cliente e servidor
typedef union {
  float floatingPoint;
  byte binary[4];
} binaryFloat;

// Variável que armazena a velocidade utilizada nos motores
binaryFloat velocidade;

// Variável utilizada para armazenar os dados que são retornados ao cliente
binaryFloat dado_retorno;

// Endereço para comunicação com o sensor MPU6050
const int MPU6050=0x68;

// Definição de variáveis para representação numérica dos erros pré-definidos no projeto
const float erro0 = 10000000;
const float erro1 = 10000001;
const float erro2 = 10000002;

// Pinos para os Motores
byte PIN_ENA = 255;
byte PIN_M1 = 255;
byte PIN_M2 = 255;
byte PIN_M3 = 255;
byte PIN_M4 = 255;
byte PIN_ENB = 255;

// Pinos para sensor do tipo Ultrassônico
byte PIN_ECHO = 255;
byte PIN_TRIG = 255;

// Pinos para Leds simples
byte PIN_LED1 = 255;
byte PIN_LED2 = 255;

// Pinos para o Led RGB
byte PIN_LEDR = 255;
byte PIN_LEDG = 255; 
byte PIN_LEDB = 255;

// Pino para o buzzer elétrico
byte PIN_TONE = 255;

// Pinos para sensores do tipo Fotoresistor
byte PIN_FR1 = 255;
byte PIN_FR2 = 255;

// Pinos para sensores do tipo Óptico Reflexivo
byte PIN_OR1 = 255;
byte PIN_OR2 = 255;
byte PIN_OR3 = 255;

// Pino para o Potenciometro
byte PIN_PTC = 255;

// Pino para Push Button
byte PIN_PBT = 255;

// Pinos para Sensor MPU
byte PIN_MPU1 = 255;
byte PIN_MPU2 = 255;

// FUNÇÕES DE CONFIGURAÇÃO //

void resetarPinos(){
  // Configuração de todos os pinos para o valor padrão
  PIN_ENA = 255;
  PIN_M1 = 255;
  PIN_M2 = 255;
  PIN_M3 = 255;
  PIN_M4 = 255;
  PIN_ENB = 255;
  PIN_ECHO = 255;
  PIN_TRIG = 255;
  PIN_LED1 = 255;
  PIN_LED2 = 255;
  PIN_LEDR = 255;
  PIN_LEDG = 255; 
  PIN_LEDB = 255;
  PIN_TONE = 255;
  PIN_FR1 = 255;
  PIN_FR2 = 255;
  PIN_OR1 = 255;
  PIN_OR2 = 255;
  PIN_OR3 = 255;
  PIN_PTC = 255;
  PIN_PBT = 255;
  PIN_MPU1 = 255;
  PIN_MPU2 = 255;

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}

void verificarPinoConfigurado(){

  // Leitura do parâmetro do comando
  int n = client.parseInt();

  // Verifica qual pino deseja ser conferido e atribui o valor configurado a ele
  // para a variável com o dado de retorno para o servidor
  switch (n) {

    case (0):
      dado_retorno.floatingPoint = PIN_ENA;
      break;

    case (1):
      dado_retorno.floatingPoint = PIN_M1;
      break;

    case (2):
      dado_retorno.floatingPoint = PIN_M2;
      break;

    case (3):
      dado_retorno.floatingPoint = PIN_M3;
      break;

    case (4):
      dado_retorno.floatingPoint = PIN_M4;
      break;

    case (5):
      dado_retorno.floatingPoint = PIN_ENB;
      break;

    case (6):
      dado_retorno.floatingPoint = PIN_ECHO;
      break;

    case (7):
      dado_retorno.floatingPoint = PIN_TRIG;
      break;

    case (8):
      dado_retorno.floatingPoint = PIN_LED1;
      break;

    case (9):
      dado_retorno.floatingPoint = PIN_LED2;
      break;

    case (10):
      dado_retorno.floatingPoint = PIN_LEDR;
      break;

    case (11):
      dado_retorno.floatingPoint = PIN_LEDG;
      break;

    case (12):
      dado_retorno.floatingPoint = PIN_LEDB;
      break;

    case (13):
      dado_retorno.floatingPoint = PIN_TONE;
      break;

    case (14):
      dado_retorno.floatingPoint = PIN_FR1;
      break;

    case (15):
      dado_retorno.floatingPoint = PIN_FR2;
      break;

    case (16):
      dado_retorno.floatingPoint = PIN_OR1;
      break;

    case (17):
      dado_retorno.floatingPoint = PIN_OR2;
      break;

    case (18):
      dado_retorno.floatingPoint = PIN_OR3;
      break;

    case (19):
      dado_retorno.floatingPoint = PIN_PTC;
      break;

    case (20):
      dado_retorno.floatingPoint = PIN_PBT;
      break;

    case (21):
      dado_retorno.floatingPoint = PIN_MPU1;
      break;

    case (22):
      dado_retorno.floatingPoint = PIN_MPU2;
      break;

    default:
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro1;
      break;
  }
  
}

void configurarMotores(){
  
  // Leitura dos parâmetros do comando para configuração das variáveis de pinagem
  PIN_ENA = client.parseInt();
  PIN_M1 = client.parseInt();
  PIN_M2 = client.parseInt();
  PIN_M3 = client.parseInt();
  PIN_M4 = client.parseInt();
  PIN_ENB = client.parseInt();

  // Validação dos parâmetros do comando
  if ((PIN_ENA < 0 || PIN_ENA > 19) || (PIN_ENB < 0 || PIN_ENB > 19) || (PIN_M1 < 0 || PIN_M1 > 19) || (PIN_M2 < 0 || PIN_M2 > 19) || (PIN_M3 < 0 || PIN_M3 > 19) || (PIN_M4 < 0 || PIN_M4 > 19)){
    // Em caso de erro, notificar o cliente e resetar os pinos do motor para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_ENA = 255;
    PIN_M1 = 255;
    PIN_M2 = 255;
    PIN_M3 = 255;
    PIN_M4 = 255;
    PIN_ENB = 255;
    return;
  }

  // Configuração dos pinos do Arduíno
  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_M1, OUTPUT);
  pinMode(PIN_M2, OUTPUT);
  pinMode(PIN_M3, OUTPUT);
  pinMode(PIN_M4, OUTPUT);
  pinMode(PIN_ENB, OUTPUT);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
}

void configurarSensorUltrassonico(){
  // Leitura dos parâmetros do comando para configuração das variáveis de pinagem
  PIN_ECHO = client.parseInt();
  PIN_TRIG = client.parseInt();

  // Validação dos parâmetros do comando
  if ((PIN_ECHO < 0 || PIN_ECHO > 19) || (PIN_TRIG < 0 || PIN_TRIG > 19)){
    // Em caso de erro, notificar o cliente e resetar os pinos para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_ECHO = 255;
    PIN_TRIG = 255;
    return;
  }
  // Configuração dos pinos do Arduíno
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_TRIG, OUTPUT);
  digitalWrite(PIN_TRIG, LOW);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
}

void configurarLedSimples(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();
  int pin = client.parseInt();

  // Validação dos parâmetros do comando
  if (pin < 0 || pin > 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configuração dos pinos do Arduíno e das variáveis de pinagem conforme parâmetros
  if (n == 1){
    PIN_LED1 = pin;
    pinMode(PIN_LED1, OUTPUT);
  }
  
  else if (n == 2){
    PIN_LED2 = pin;
    pinMode(PIN_LED2, OUTPUT);
  }

  else {
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}

void configurarLedRGB(){

  // Leitura dos parâmetros do comando para configuração das variáveis de pinagem
  PIN_LEDR = client.parseInt();
  PIN_LEDG = client.parseInt();
  PIN_LEDB = client.parseInt();

  // Validação dos parâmetros do comando
  if ((PIN_LEDR < 0 || PIN_LEDR > 19) || (PIN_LEDG < 0 || PIN_LEDG > 19) || (PIN_LEDB < 0 || PIN_LEDB > 19)){
    // Em caso de erro, notificar o cliente e resetar os pinos do motor para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_LEDR = 255;
    PIN_LEDG = 255;
    PIN_LEDB = 255;
    return;
  }

  // Configuração dos pinos do Arduíno
  pinMode(PIN_LEDR, OUTPUT);
  pinMode(PIN_LEDG, OUTPUT);
  pinMode(PIN_LEDB, OUTPUT);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}

void configurarBuzzer(){
  
  // Leitura dos parâmetros do comando para configuração das variáveis de pinagem
  PIN_TONE = client.parseInt();

  // Validação dos parâmetros do comando
  if (PIN_TONE < 0 || PIN_TONE > 19){
    // Em caso de erro, notificar o cliente e resetar os pinos do motor para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_TONE = 255;
    return;
  }
  
  // Configuração dos pinos do Arduíno
  pinMode(PIN_TONE, OUTPUT);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}
  
void configurarSensorFotoresistor(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();
  int pin = client.parseInt();

  // Validação dos parâmetros do comando
  if (pin < 0 | pin > 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configuração dos pinos do Arduíno e das variáveis de pinagem conforme parâmetros
  if (n == 1){
    PIN_FR1 = pin;
    pinMode(PIN_FR1, INPUT);
  }
  
  else if (n == 2){
    PIN_FR2 = pin;
    pinMode(PIN_FR2, INPUT);
  }

  else {
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}  

void configurarSensorOpticoReflexivo(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();
  int pin = client.parseInt();

  // Validação dos parâmetros do comando
  if (pin < 0 | pin > 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configuração dos pinos do Arduíno e das variáveis de pinagem conforme parâmetros
  if (n == 1){
    PIN_LED1 = pin;
    pinMode(PIN_OR1, OUTPUT);
  }
  
  else if (n == 2){
    PIN_LED2 = pin;
    pinMode(PIN_OR2, OUTPUT);
  }
  
  else if (n == 3){
    PIN_OR3 = pin;
    pinMode(PIN_OR3, INPUT);
  }

  else {
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
 
}
  
void configurarPotenciometro(){

  // Leitura dos parâmetros do comando para configuração das variáveis de pinagem
  PIN_PTC = client.parseInt();

  // Validação dos parâmetros do comando
  if (PIN_PTC < 0 || PIN_PTC > 19){
    // Em caso de erro, notificar o cliente e resetar os pinos do motor para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_PTC = 255;
    return;
  }
  
  // Configuração dos pinos do Arduíno
  pinMode(PIN_PTC, INPUT);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}

void configurarPushButton(){

  // Leitura dos parâmetros do comando
  PIN_PBT = client.parseInt();

  // Validação dos parâmetros do comando
  if (PIN_PBT < 0 || PIN_PBT > 19){
    // Em caso de erro, notificar o cliente e resetar os pinos do motor para o valor padrão
    dado_retorno.floatingPoint = erro1;
    PIN_PBT = 255;
    return;
  }
  
  // Configuração dos pinos do Arduíno
  pinMode(PIN_PBT, INPUT);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void configurarMPU(){
  
  // Iniciar a comunicação I2C para comunicar com o sensor MPU6050
  Wire.begin();
  Wire.beginTransmission(MPU6050);
  Wire.write(0x6B); 

  // Envio de argumento de configuração padrão e finalização da transmissão
  Wire.write(0); 
  Wire.endTransmission(true);

  // Configuração das variáveis de pinagem referentes ao sensor
  PIN_MPU1 = 18;
  PIN_MPU2 = 19;

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}
// FUNÇÕES DE AÇÕES //

void getVelocidade(){

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = velocidade.floatingPoint;

}

void setVelocidade(){
  
  // Leitura dos parâmetros do comando
  int v1 = client.parseInt();  // Lê um byte
  int v2 = client.parseInt();  // Lê um byte

  // Validação do parâmetro
  if ((v1 >= 0 && v1 <= 255) && (v2 >= 0 && v2 <= 255)){
    // Configurando a variável com o dado de retorno para o servidor
    dado_retorno.floatingPoint = 1;
    analogWrite(PIN_ENA, v1);
    analogWrite(PIN_ENB, v2);
  }
  else
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    
}

void andarParaFrente(){

  // Parando os motores
  digitalWrite(PIN_M1, HIGH);
  digitalWrite(PIN_M2, LOW);
  digitalWrite(PIN_M3, HIGH);
  digitalWrite(PIN_M4, LOW);
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void andarParaTras(){

  // Parando os motores
  digitalWrite(PIN_M1, LOW);
  digitalWrite(PIN_M2, HIGH);
  digitalWrite(PIN_M3, LOW);
  digitalWrite(PIN_M4, HIGH);
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void rotacionarEsquerda(){
  
  // Motores para esquerda
  digitalWrite(PIN_M1, HIGH);
  digitalWrite(PIN_M2, LOW);
  digitalWrite(PIN_M3, LOW);
  digitalWrite(PIN_M4, HIGH);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
}

void rotacionarDireita(){

  // Motores para direita
  digitalWrite(PIN_M1, LOW);
  digitalWrite(PIN_M2, HIGH);
  digitalWrite(PIN_M3, HIGH);
  digitalWrite(PIN_M4, LOW);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
}

void fazerCurva(){
  
  // Leitura dos parâmetros do comando (velocidades N1 e N2)
  int v1 = client.parseInt();  // Velocidade para o Motor A (PIN_ENA)
  int v2 = client.parseInt();  // Velocidade para o Motor B (PIN_ENB)

  // Validação dos parâmetros [0, 255] (ERRO 1)
  if ((v1 < 0 || v1 > 255) || (v2 < 0 || v2 > 255)){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Define as velocidades diferentes para cada motor
  analogWrite(PIN_ENA, v1);
  analogWrite(PIN_ENB, v2);
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void pararMotores(){

  // Código para parar os motores
  digitalWrite(PIN_M1, LOW);
  digitalWrite(PIN_M2, LOW);
  digitalWrite(PIN_M3, LOW);
  digitalWrite(PIN_M4, LOW);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void ativarLed(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();

  // Identificação de qual Led deve ser acionado
  if (n == 1 && PIN_LED1 != 255)
    // Acionamenrto do Led
    digitalWrite(PIN_LED1, HIGH);
  
  else if (n == 2 && PIN_LED2 != 255)
    digitalWrite(PIN_LED2, HIGH);
  
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_LED1 == 255 || PIN_LED2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
 
}  

void ativarLedDelay(){
  
  // Leitura dos parâmetros do comando
  int n = client.parseInt();
  unsigned int tempo_atraso_ms = client.parseInt();

  // Identificação de qual Led deve ser acionado
  if (n == 1 && PIN_LED1 != 255){
    // Acionamenrto do Led
    digitalWrite(PIN_LED1, HIGH);
    // Acionamento do delay conforme parâmetro
    delay(tempo_atraso_ms);
    // Desacionamento do Led
    digitalWrite(PIN_LED1, LOW);
  }
  
  else if (n == 2 && PIN_LED2 != 255){
    digitalWrite(PIN_LED2, HIGH);
    delay(tempo_atraso_ms);
    digitalWrite(PIN_LED2, LOW);
  }
  
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_LED1 == 255 || PIN_LED2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}  

void inverterLed(){
  
  // Leitura dos parâmetros do comando
  int n = client.parseInt();

  // Identificação de qual Led deve ser acionado
  if (n == 1 && PIN_LED1 != 255)
    // Enviando sinal contrário ao atual para o led -> inverter seu estado
    digitalWrite(PIN_LED1, !digitalRead(PIN_LED1));
  
  else if (n == 2 && PIN_LED2 != 255)
    digitalWrite(PIN_LED2, !digitalRead(PIN_LED2));
  
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_LED1 == 255 || PIN_LED2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void desativarLed(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();

  // Identificação de qual Led deve ser desativado
  if (n == 1 && PIN_LED1 != 255)
    digitalWrite(PIN_LED1, LOW);
  
  else if (n == 2 && PIN_LED2 != 255)
    digitalWrite(PIN_LED2, LOW);
  
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_LED1 == 255 || PIN_LED2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
    
}

void ativarLedRGB(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_LEDR == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return; 
  }
  
  // Leitura dos parâmetros do comando
  int r = client.parseInt();
  int g = client.parseInt();
  int b = client.parseInt();

  // Validação dos parâmetros
  if (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255){
  
    // Ativando o Led RGB conforme valores passados por parâmetro
    analogWrite(PIN_LEDR, r);
    analogWrite(PIN_LEDG, g);
    analogWrite(PIN_LEDB, b);

    // Configurando a variável com o dado de retorno para o servidor
    dado_retorno.floatingPoint = 1;
  }
  else
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1;   
 
}

void ativarLedRGBDelay(){
  
  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_LEDR == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return; 
  }
  
  // Leitura dos parâmetros do comando
  int r = client.parseInt();
  int g = client.parseInt();
  int b = client.parseInt();
  unsigned int tempo_atraso_ms = client.parseInt();

  if (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255){
  
    // Ativando o Led RGB conforme valores passados por parâmetro
    analogWrite(PIN_LEDR, r);
    analogWrite(PIN_LEDG, g);
    analogWrite(PIN_LEDB, b);
    
    // Ativando o delay conforme valor passado por parâmetro
    delay(tempo_atraso_ms);
    
    // Desativando o Led RGB
    analogWrite(PIN_LEDR, 0);
    analogWrite(PIN_LEDG, 0);
    analogWrite(PIN_LEDB, 0);

    // Configurando a variável com o dado de retorno para o servidor
    dado_retorno.floatingPoint = 1;
  }
  else
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro1; 
    
}
    
void desativarLedRGB(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_LEDR == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return; 
  }

  // Desativando o Led RGB
  analogWrite(PIN_LEDR, 0);
  analogWrite(PIN_LEDG, 0);
  analogWrite(PIN_LEDB, 0);

  dado_retorno.floatingPoint = 1;
}

void ativarBuzzer(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_TONE == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Leitura dos parâmetros do comando
  unsigned int frequencia = client.parseInt();
  
  // Ativando o buzzer
  tone(PIN_TONE, frequencia);
  
  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
}
  

void ativarBuzzerDelay(){
  
  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_TONE == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Leitura dos parâmetros do comando
  unsigned int frequencia = client.parseInt();
  unsigned int tempo_atraso_ms = client.parseInt();
  
  // Ativando o buzzer
  tone(PIN_TONE, frequencia);
  
  // Ativando o delay conforme valor passado por parâmetro
  delay(tempo_atraso_ms);
  
  // Desativando o Buzzer
  noTone(PIN_TONE);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;
  
}

void desativarBuzzer(){
  
  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_TONE == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  
  // Desativando o Buzzer
  noTone(PIN_TONE);

  // Configurando a variável com o dado de retorno para o servidor
  dado_retorno.floatingPoint = 1;

}

void lerSensorUltrassonico(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_TRIG == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  
  // Ativando a emissão da onda ultrassônica
  digitalWrite(PIN_TRIG, HIGH);
  // Aguardando um delay
  delayMicroseconds(10);
  // Desativando a emissão da onda ultrassônica
  digitalWrite(PIN_TRIG, LOW);
  
  // Configurando a variável com o dado de retorno do sensor ultrassônico para o servidor
  dado_retorno.floatingPoint = pulseIn(PIN_ECHO, HIGH)/2 * 0.034029;

}

void lerSensorFotoresistor(){

  // Leitura dos parâmetros do comando
  int n = client.parseInt();

  // Identificado qual sensor fotoresistor foi selecionado
  if (n == 1 && PIN_FR1 != 255)
    // Configurando a variável com o dado de retorno do sensor para o servidor
    dado_retorno.floatingPoint = analogRead(PIN_FR1);
  else if (n == 2 && PIN_FR2 != 255)
    dado_retorno.floatingPoint = analogRead(PIN_FR2);
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_FR1 == 255 || PIN_FR2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }

}

void lerSensorOpticoReflexivo(){
  
  // Leitura dos parâmetros do comando
  int n = client.parseInt();

  // Identificando qual sensor óptico reflexivo foi selecionado
  if (n == 1 && PIN_OR1 != 255)
    // Configurando a variável com o dado de retorno do sensor para o servidor
    dado_retorno.floatingPoint = digitalRead(PIN_OR1);
  else if (n == 2 && PIN_OR2 != 255)
    dado_retorno.floatingPoint = digitalRead(PIN_OR2);
  else if (n == 3 && PIN_OR3 != 255)
    dado_retorno.floatingPoint = digitalRead(PIN_OR3);
  else {
    // Verifica se os pinos requeridos para essa ação foram configurados
    if ((PIN_FR1 == 255 || PIN_FR2 == 255) && (n == 1 || n == 2)){
      // Em caso de erro, notificar o cliente
      dado_retorno.floatingPoint = erro0;
      return; 
    }
    
    // Em caso de erro no valor de n, notificar o cliente
    dado_retorno.floatingPoint = erro1;
    return;
  }
    
}
  
void lerPotenciometro(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_PTC == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  
  // Configurando a variável com o dado de retorno do sensor para o servidor
  dado_retorno.floatingPoint = analogRead(PIN_PTC);
  
}
  
void lerBotao(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_PBT == 255){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Configurando a variável com o dado de retorno do sensor para o servidor
  dado_retorno.floatingPoint = digitalRead(PIN_PBT);
  
}
  
void lerTemperatura(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  
  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);

  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  
  // Configurando a variável com o dado de retorno do sensor para o servidor
  dado_retorno.floatingPoint = Wire.read()<<8|Wire.read();
  // Conversão do retorno para formato especificado na documentação
  dado_retorno.floatingPoint = dado_retorno.floatingPoint/340.00+36.53;
  
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
 
}

void lerAcelerometroX(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/16384*9.80665;      
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  
}

void lerAcelerometroY(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/16384*9.80665;
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  
}

void lerAcelerometroZ(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  Wire.read()<<8|Wire.read(); 
  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/16384*9.80665;
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  
}

void lerGiroscopioX(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/131*0.0174533; 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  
}

void lerGiroscopioY(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }

  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/131*0.0174533;
  Wire.read()<<8|Wire.read(); 
  
}

void lerGiroscopioZ(){

  // Verifica se os pinos requeridos para essa ação foram configurados
  if (PIN_MPU1 != 18 || PIN_MPU2 != 19){
    // Em caso de erro, notificar o cliente
    dado_retorno.floatingPoint = erro0;
    return;
  }
  
  // Iniciando comunicação com o sensor MPU-6050
  Wire.beginTransmission(MPU6050);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  
  // Requisitando os bytes com os dados de leitura do servidor
  Wire.requestFrom(MPU6050,14,true);
  
  // Percorrendo os bytes do retorno para obter apenas aqueles
  // que condizem com a função atual

  Wire.read()<<8|Wire.read();      
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  Wire.read()<<8|Wire.read(); 
  // Configurando a variável com o dado de retorno formatado do sensor para o servidor
  dado_retorno.floatingPoint = (Wire.read()<<8|Wire.read())/131*0.0174533; 
  
}

void encerrarComunicacao(){
  NVIC_SystemReset();
}

void setup() {
  Serial.begin(115200);
  // Configurando a velocidade para o seu valor inicial padrão
  velocidade.floatingPoint = 255;
  
  // Iniciando o dispositivo para comunicação Wifi
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

  // --- Descoberta via UDP ---
  while (!pcConectado) {
    int packetSize = udp.parsePacket();
    if (packetSize) {
      int len = udp.read(incomingPacket, 254);
      incomingPacket[len] = '\0';
      Serial.print("Recebido (descoberta): ");
      Serial.println(incomingPacket);


      if (strcmp(incomingPacket, "UnoR4WiFi") == 0) {
        pcIP = udp.remoteIP();
        pcPort = udp.remotePort();
        pcConectado = true;

        udp.beginPacket(pcIP, pcPort);
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

  // Flag para verificar se o ciclo de configuração deve ser finalizado
  bool configuradoGeral = false;
  
  while (!configuradoGeral){

    // Se algum byte foi recebido pelo servidor  
    if (client && client.available()) {
      
      // Ler byte
      byte c = client.read();
      
      // Interpretar byte e executar respectiva função
      switch (c){

        case (42):
          // Finalizar configuração inicial
          configuradoGeral = true;
          // Configurando a variável com o dado de retorno para o servidor
          dado_retorno.floatingPoint = 1;
          break;

        case (77):
          configurarMotores();
          break;

        case (85):
          configurarSensorUltrassonico();
          break;

        case (83):
          configurarLedSimples();
          break;

        case (76):
          configurarLedRGB();
          break;

        case (90):
          configurarBuzzer();
          break;

        case (70):
          configurarSensorFotoresistor();
          break;

        case (79):
          configurarSensorOpticoReflexivo();
          break;

        case (80):
          configurarPotenciometro();
          break;

        case (66):
          configurarPushButton();
          break;

        case (88):
          configurarMPU();
          break;

        case (82):
          resetarPinos();
          break;

        case (86):
          verificarPinoConfigurado();
          break;

        default:
          // Em caso de erro, notificar o cliente
          dado_retorno.floatingPoint = erro2;
          break;
      }
      // Enviando os bytes do dado de retorno ao cliente
      client.write(dado_retorno.binary, 4);
    
    }
  }

  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_ENB, OUTPUT);
  analogWrite(PIN_ENA, 128);
  analogWrite(PIN_ENB, 128);
  
}

void loop() {
  
  // Verifica se algum byte foi enviado ao servidor
  if (client && client.available()) {

    //Faz a leitura dos dois bytes
    byte c1 = client.read();
    byte c2 = client.read();
    // Interpreta o primeiro byte
    switch (c1) {

      case (86):
        
        // Interpreta o segundo byte
        if (c2 == 71)
          getVelocidade();

        else if (c2 == 83)
          setVelocidade();
        else
          // Em caso de erro, notificar o cliente
          dado_retorno.floatingPoint = erro2;
        break;

      case (77):

        // Interpreta o segundo byte
        switch (c2) {

          case (80):
            pararMotores();
            break;

          case (70):
            andarParaFrente();
            break;
          
          case (84):
            andarParaTras();
            break;
          
          case (68):
            rotacionarDireita();
            break;
          
          case (69):
            rotacionarEsquerda();
            break;
          
          case (67):
            fazerCurva();
            break;
            
          default:
            // Em caso de erro, notificar o cliente
            dado_retorno.floatingPoint = erro2;
            break;
          
        }
        break;

      case (82):

        switch (c2){

          case (85):
            lerSensorUltrassonico();
            break;

          case (70):
            lerSensorFotoresistor();
            break;

          case (79):
            lerSensorOpticoReflexivo();
            break;

          case (80):
            lerPotenciometro();
            break;

          case (66):
            lerBotao();
            break;

          case (84):
            lerTemperatura();
            break;

          case (65):
            lerAcelerometroX();
            break;

          case (67):
            lerAcelerometroY();
            break;

          case (69):
            lerAcelerometroZ();
            break;

          case (71):
            lerGiroscopioX();
            break;

          case (73):
            lerGiroscopioY();
            break;

          case (75):
            lerGiroscopioZ();
            break;

          default:
            dado_retorno.floatingPoint = erro2;
            break;
        }
        break;

      case (83):

        switch (c2){
        
          case (65):
            ativarLed();
            break;

          case (84):
            ativarLedDelay();
            break;

          case (73):
            inverterLed();
            break;

          case (68):
            desativarLed();
            break;

          default:
            dado_retorno.floatingPoint = erro2;
            break;
            
        }
        break;

      case (76):

        switch (c2){
          
          case (65):
            ativarLedRGB();
            break;

          case (84):
            ativarLedRGBDelay();
            break;

          case (68):
            desativarLedRGB();
            break;

          default:
            dado_retorno.floatingPoint = erro2;
            break;
        }
        break;

      case (90):

        switch (c2){

          case (65):
            ativarBuzzer();
            break;

          case (84):
            ativarBuzzerDelay();
            break;

          case (68):
            desativarBuzzer();
            break;
            
          default:
            dado_retorno.floatingPoint = erro2;
            break;
        }
        break;

      case (69):

        if (c2 == 82)
          encerrarComunicacao();
        else
          dado_retorno.floatingPoint = erro2;
        break;
      
      default:
        dado_retorno.floatingPoint = erro2;
        break;
    }
    
    // Enviando os bytes do dado de retorno ao cliente
    client.write(dado_retorno.binary, 4);
  }
  
  delay(2);
  
}