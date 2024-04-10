from microbit import *
from random import choice

#Configura la cuadricula del Tetris
grid=[[1,0,0,0,0,0,1],[1,0,0,0,0,0,1],[1,0,0,0,0,0,1],[1,0,0,0,0,0,1],[1,0,0,0,0,0,1],[1,1,1,1,1,1,1]]
#Almacena una lista de 4 bloques, cada bloque es una cuadrícula de 2x2
bricks = [[9,9],[9,0]],[[9,9],[0,9]],[[9,9],[9,9]],[[9,9],[0,0]]
#Selecciona un bloque al azar y lo coloca en el centro/parte superior del display LED (y=0,x=3)
brick = choice(bricks)
x=3
y=0
frameCount=0

#Función para devolver un máximo de 2 valores
def max(a,b):
    if a>=b:
        return a
    else:
        return b
        
#Función para ocultar el bloque de 2x2 en el display LED
def hideBrick():
    if x>0:
        display.set_pixel(x-1,y,grid[y][x])
    if x<5:
        display.set_pixel(x+1-1,y,grid[y][x+1])
    if x>0 and y<4:
        display.set_pixel(x-1,y+1,grid[y+1][x])
    if x<5 and y<4:
        display.set_pixel(x+1-1,y+1,grid[y+1][x+1])
        
#Función para mostrar el bloque de 2x2 en el display LED
def showBrick():
    if x>0:
        display.set_pixel(x-1,y,max(brick[0][0],grid[y][x]))
    if x<5:
        display.set_pixel(x+1-1,y,max(brick[0][1],grid[y][x+1]))
    if x>0 and y<4:
        display.set_pixel(x-1,y+1,max(brick[1][0],grid[y+1][x]))
    if x<5 and y<4:
        display.set_pixel(x+1-1,y+1,max(brick[1][1],grid[y+1][x+1]))

#Función para rotar el bloque 2x2
def rotateBrick():
    pixel00 = brick[0][0]
    pixel01 = brick[0][1]
    pixel10 = brick[1][0]
    pixel11 = brick[1][1]
    #Comprueba si la rotación es posible
    if not ((grid[y][x]>0 and pixel00>0) or (grid[y+1][x]>0 and pixel10>0) or (grid[y][x+1]>0 and pixel01>0) or (grid[y+1][x+1]>0 and pixel11>0)):
        hideBrick()
        brick[0][0] = pixel10
        brick[1][0] = pixel11
        brick[1][1] = pixel01
        brick[0][1] = pixel00
        showBrick()

#Función para mover el bloque
def moveBrick(delta_x,delta_y):
    global x,y
    move=False
    #Comprueba si el movimiento es posible: no choca con otros bloques ni con los bordes del display.
    if delta_x==-1 and x>0:
        if not ((grid[y][x-1]>0 and brick[0][0]>0) or (grid[y][x+1-1]>0 and brick[0][1]>0) or (grid[y+1][x-1]>0 and brick[1][0]>0) or (grid[y+1][x+1-1]>0 and brick[1][1]>0)):
            move=True
    elif delta_x==1 and x<5:
        if not ((grid[y][x+1]>0 and brick[0][0]>0) or (grid[y][x+1+1]>0 and brick[0][1]>0) or (grid[y+1][x+1]>0 and brick[1][0]>0) or (grid[y+1][x+1+1]>0 and brick[1][1]>0)):
            move=True
    elif delta_y==1 and y<4:
        if not ((grid[y+1][x]>0 and brick[0][0]>0) or (grid[y+1][x+1]>0 and brick[0][1]>0) or (grid[y+1+1][x]>0 and brick[1][0]>0) or (grid[y+1+1][x+1]>0 and brick[1][1]>0)):
            move=True
    #Si el movimiento es posible, actualiza las coordenadas x,y del bloque
    if move:
        hideBrick()
        x+=delta_x
        y+=delta_y
        showBrick()
        
    #Devuelve True o False para confirmar si el movimiento se ha realizado
    return move

#A function to check for and remove completed lines
def checkLines():
    global score
    removeLine=False
    #Comprueba cada linea de una en una
    for i in range(0, 5):
        #Si se rellenan 5 bloques (9), una línea está completa
        if (grid[i][1]+grid[i][2]+grid[i][3]+grid[i][4]+grid[i][5])==45:
            removeLine = True
            #Incrementa la puntuación (10 puntos por linea)
            score+=10
            #Elimina la linea y hace que todas las lineas superiores caigan 1 puesto
            for j in range(i,0,-1):
                grid[j] = grid[j-1]
            grid[0]=[1,0,0,0,0,0,1]
    if removeLine:
        #Actualiza el display LED
        for i in range(0, 5):
            for j in range(0, 5):
                display.set_pixel(i,j,grid[j][i+1])
    return removeLine
    
gameOn=True
score=0
showBrick()
#Bucle del programa principal - itera cada 50ms
while gameOn:
    sleep(50)
    frameCount+=1
    #Captura el input del usuario
    if button_a.is_pressed() and button_b.is_pressed():
        rotateBrick()
    elif button_a.is_pressed():
        moveBrick(-1,0)
    elif button_b.is_pressed():
        moveBrick(1,0)
    
    #Cada 15 frames, se intenta mover el bloque abajo
    if frameCount==15 and moveBrick(0,1) == False:
        frameCount=0
        #El movimiento no ha sido posible, el bloque se mantiene en la misma posición
        grid[y][x]=max(brick[0][0],grid[y][x])
        grid[y][x+1]=max(brick[0][1],grid[y][x+1])
        grid[y+1][x]=max(brick[1][0],grid[y+1][x])
        grid[y+1][x+1]=max(brick[1][1],grid[y+1][x+1])
        
        if checkLines()==False and y==0:
            #El bloque ha alcanzado el top del display LED - Perdiste
            gameOn=False
        else:
            #Selecciona un nuevo bloque aleatoriamente
            x=3
            y=0
            brick = choice(bricks)
            showBrick()
    
    if frameCount==15:
       frameCount=0

#Fin del juego
sleep(2000)
display.scroll("Game Over: Score: " + str(score))