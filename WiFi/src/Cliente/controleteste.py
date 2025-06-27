import pygame


pygame.init()
pygame.joystick.init()


if pygame.joystick.get_count() == 0:
    print("Nenhum controle encontrado.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Controle detectado: {joystick.get_name()}")

while True:
    pygame.event.pump()  

    eixo_x = joystick.get_axis(0)
    eixo_y = joystick.get_axis(1)
    print(f"Eixo X: {eixo_x:.2f}, Eixo Y: {eixo_y:.2f}")
    lt = joystick.get_axis(2)  
    rt = joystick.get_axis(5)  

    print(f"LT: {lt:.2f}, RT: {rt:.2f}")

    pygame.time.wait(5)  
