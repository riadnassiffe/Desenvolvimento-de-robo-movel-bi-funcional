"""
Módulo de Comandos - Protocolo Serial do Robô.

Este arquivo centraliza todas as strings de comando (códigos de protocolo)
usadas na comunicação entre o script Python e o robô (ex: Arduino).

O objetivo é mapear constantes Python legíveis (ex: MOVER_PARA_FRENTE)
para os códigos de string curtos (ex: "MF") que o robô espera.

Fica a gosto do usuário utilizar os comandos ou diretamente suas representações
de letras.
"""

# --- Comandos de Configuração setup() ---
CONFIGURAR_MOTORES = "M"            # configurarMotores()
CONFIGURAR_ULTRASSONICO = "U"       # configurarSensorUltrassonico()
CONFIGURAR_LED_SIMPLES = "S"        # configurarLedSimples()
CONFIGURAR_LED_RGB = "L"            # configurarLedRGB()
CONFIGURAR_BUZZER = "Z"             # configurarBuzzer()
CONFIGURAR_FOTORESISTOR = "F"       # configurarSensorFotoresistor()
CONFIGURAR_OPTICO = "O"             # configurarSensorOpticoReflexivo()
CONFIGURAR_POTENCIOMETRO = "P"      # configurarPotenciometro()
CONFIGURAR_BOTAO = "B"              # configurarPushButton()
CONFIGURAR_MPU = "X"                # configurarMPU()
RESETAR_PINOS = "R"                 # resetarPINos()
VERIFICAR_PINO_CONFIGURADO = "V"    # verificarPINoConfigurado()
SETUP_CONCLUIDO = "*"               # Finaliza o loop de configuração

# --- Comandos de Ação loop() ---
# --- Sistema ---
FINALIZAR = "ER"                    # encerrarComunicacao()

# --- Velocidade ---
GET_VELOCIDADE = "VG"               # getVelocidade()
SET_VELOCIDADE = "VS"               # setVelocidade()

# --- Motores ---
MOTOR_PARAR = "MP"                  # pararMotores()
MOVER_PARA_FRENTE = "MF"            # andarParaFrente()
MOVER_PARA_TRAZ = "MT"              # andarParaTras()
MOVER_PARA_DIREITA = "MD"           # rotacionarDireita()
MOVER_PARA_ESQUERDA = "ME"          # rotacionarEsquerda()
MOVER_CURVA = "MC"                  # fazerCurva()

# --- Leitura de Sensores ---
SENSOR_ULTRASSONICO = "RU"          # lerSensorUltrassonico()
LER_FOTORESISTOR = "RF"             # lerSensorFotoresistor()
LER_OPTICO = "RO"                   # lerSensorOpticoReflexivo()
LER_POTENCIOMETRO = "RP"            # lerPotenciometro()
LER_BOTAO = "RB"                    # lerBotao()
LER_TEMPERATURA = "RT"              # lerTemperatura()
LER_ACELEROMETRO_X = "RA"           # lerAcelerometroX()
LER_ACELEROMETRO_Y = "RC"           # lerAcelerometroY()
LER_ACELEROMETRO_Z = "RE"           # lerAcelerometroZ()
LER_GIROSCOPIO_X = "RG"             # lerGiroscopioX()
LER_GIROSCOPIO_Y = "RI"             # lerGiroscopioY()
LER_GIROSCOPIO_Z = "RK"             # lerGiroscopioZ()

# --- LED Simples ---
LED_SIMPLES_ATIVAR = "SA"           # ativarLed()
LED_SIMPLES_ATIVAR_DELAY = "ST"     # ativarLedDelay()
LED_SIMPLES_INVERTER = "SI"         # inverterLed()
LED_SIMPLES_DESATIVAR = "SD"        # desativarLed()

# --- LED RGB ---
LED_RGB_ATIVAR = "LA"               # ativarLedRGB()
LED_RGB_ATIVAR_DELAY = "LT"         # ativarLedRGBDelay()
LED_RGB_DESATIVAR = "LD"            # desativarLedRGB()

# --- Buzzer ---
BUZZER_ATIVAR = "ZA"                # ativarBuzzer()
BUZZER_ATIVAR_DELAY = "ZT"          # ativarBuzzerDelay()
BUZZER_DESATIVAR = "ZD"             # desativarBuzzer()

# Porta do Arduino
PIN1 = "1"
PIN2 = "2"
PIN3 = "3"
PIN4 = "4"
PIN5 = "5"
PIN6 = "6"
PIN7 = "7"
PIN8 = "8"
PIN9 = "9"
PIN10 = "10"
PIN11 = "11"
PIN12 = "12"
PIN13 = "13"
PIN14 = "14"