def changeLedState (NewState):
    global x_position
    global y_position
    global tetris
    global block
    
    if NewState is True : #Muestra el bloque actual
        if x_position > 0 :
            led.plot_brightness(x_position - 1, y_position, max(block[0][0], tetris[y_position][x_position]))
        if x_position < 5:
            led.plot_brightness((x_position - 1) + 1, y_position, max(block[0][1], tetris[y_position][x_position + 1]))
        if x_position > 0 and y_position < 4:
            led.plot_brightness(x_position - 1, y_position + 1, max(block[1][0], tetris[y_position + 1][x_position]))
        if x_position < 5 and y_position < 4:
            led.plot_brightness((x_position - 1) + 1, y_position + 1, max(block[1][1], tetris[y_position + 1][x_position + 1]))
    else: #Oculta el bloque actual
        if x_position > 0 :
            led.plot_brightness(x_position - 1, y_position, tetris[y_position][x_position])
        if x_position < 5 :
            led.plot_brightness((x_position - 1) + 1, y_position, tetris[y_position][x_position + 1])
        if x_position > 0 and y_position < 4:
            led.plot_brightness(x_position - 1, y_position + 1, tetris[y_position + 1][x_position])
        if x_position < 5 and y_position < 4:
            led.plot_brightness((x_position - 1) + 1, y_position + 1, tetris[y_position + 1][x_position + 1])
    pass

#Aplica la rotación a la posición del bloque actual
def rotateblock():
    global x_position
    global y_position
    global tetris
    global block
    #Comprueba si la rotación es posible
    if not (
            (tetris[y_position][x_position] > 0 and block[0][0] > 0)
            or (tetris[y_position + 1][x_position] > 0 and block[1][0] > 0)
            or (tetris[y_position][x_position + 1] > 0 and block[0][1] > 0)
            or (tetris[y_position + 1][x_position + 1] > 0 and block[1][1] > 0)
    ):
        #Oculta el bloque para aplicar la rotación
        #hideblock()
        changeLedState(False)
        #Aplica la rotación
        block00 = block[0][0]
        block[0][0] = block[1][0]
        block[1][0] = block[1][1]
        block[1][1] = block[0][1]
        block[0][1] = block00
        #showblock()
        changeLedState(True)

#Mueve el bloque en el eje X (Izquierda y Derecha) y en el eje Y (abajo)
def moveBlock(x_move, y_move):
    global x_position, y_position
    move = False
    
    #Verifica que el movimiento es posible
    if x_move == -1 and x_position > 0:
        if not (
                (tetris[y_position][x_position - 1] > 0 and block[0][0] > 0)
                or (tetris[y_position][x_position + 1 - 1] > 0 and block[0][1] > 0)
                or (tetris[y_position + 1][x_position - 1] > 0 and block[1][0] > 0)
                or (tetris[y_position + 1][x_position + 1 - 1] > 0 and block[1][1] > 0)
        ):
            move = True
    elif x_move == 1 and x_position < 5:
        if not ((tetris[y_position][x_position + 1] > 0 and block[0][0] > 0) or (tetris[y_position][x_position + 1 + 1] > 0 and block[0][1] > 0) or (
                tetris[y_position + 1][x_position + 1] > 0 and block[1][0] > 0) or (tetris[y_position + 1][x_position + 1 + 1] > 0 and block[1][1] > 0)):
            move = True
    elif y_move == 1 and y_position < 4:
        if not ((tetris[y_position + 1][x_position] > 0 and block[0][0] > 0) or (tetris[y_position + 1][x_position + 1] > 0 and block[0][1] > 0) or (
                tetris[y_position + 1 + 1][x_position] > 0 and block[1][0] > 0) or (tetris[y_position + 1 + 1][x_position + 1] > 0 and block[1][1] > 0)):
            move = True
    
    #Si el movimiento es posible, se puede actualizar los ejes X e Y del bloque
    if move:
        changeLedState(False)
        #hideblock()
        x_position += x_move
        y_position += y_move
        changeLedState(True)

    #Devuelve True o False si el movimiento del bloque es posible
    return move


def moveblockLeft():
    x_move = -1
    y_move = 0
    moveBlock(x_move, y_move)


def moveblockRight():
    x_move = 1
    y_move = 0
    return moveBlock(x_move, y_move)

def moveblockDown():
    x_move = 0
    y_move = 1
    return moveBlock(x_move, y_move)

#Comprueba las lineas si alguna esta completa
def checkCompletedLines():
    global x_position
    global y_position
    global tetris
    global block
    global score
    removeLine = False

    #Comprueba cada linea de una en una
    for i in range(0, 5):
        
        #Si una linea ha sido completada entonces esta deberá de ser eliminada y la puntuación aumentada
        if (tetris[i][1] + tetris[i][2] + tetris[i][3] + tetris[i][4] + tetris[i][5]) == on_led_value * 5:
            removeLine = True
            
            #Incrementa la puntuación
            score += winingScore
            
            #Elimina la linea y hace que las superiores caigan
            for j in range(i, 0, -1):
                tetris[j] = tetris[j - 1]
            tetris[0] = [1, 0, 0, 0, 0, 0, 1]
    if removeLine:
        #Actualiza el display LED
        for i in range(0, 5):
            for j in range(0, 5):
                led.plot_brightness(i, j, tetris[j][i + 1])
    return removeLine

def play_music():
    music.start_melody(music.built_in_melody(Melodies.DADADADUM))

def on_gesture_shake():
    control.reset()
    pass


def init_game():
    #Mensaje de inicio
    basic.show_number(3)
    basic.show_number(2)
    basic.show_number(1)
    basic.show_string("GO")

    #Eventos --------------------------------------------

    #Evento del boton táctil
    input.on_logo_event(TouchButtonEvent.PRESSED, rotateblock)

    #Evento de los botones
    input.on_button_pressed(Button.A, moveblockLeft)
    input.on_button_pressed(Button.B, moveblockRight)
    
    #Micrófono
    #play_music()
    
    #Giroscopio
    input.on_gesture(Gesture.SHAKE, on_gesture_shake)
    # --------------------------------------------



#Starteo de programa -------------------------------------------->>>>>>>>>>>>
init_game()
#Intensidad máxima del LED
on_led_value = 255
#Puntuacion que se añade cuando se complete una linea
winingScore = 10
#Crea una matriz del tetris
tetris = [[1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]

#Crea las posibilidades del generamiento de bloques
blocks = [[on_led_value, on_led_value], [on_led_value, 0]], [[on_led_value, on_led_value], [0, on_led_value]], [
    [on_led_value, on_led_value], [on_led_value, on_led_value]], [[on_led_value, on_led_value], [0, 0]]

#Selecciona el bloque aleatoriamente
block = blocks[randint(0, blocks.length - 1)]

#Posicion inicial del primer bloque
x_position = 2
y_position = 0
coutFrame = 0


gameOn = True
score = 0
changeLedState(True)

#Bucle del programa principal - itera cada 50ms
def on_forever():
    global gameOn
    global x_position
    global y_position
    global tetris
    global block
    global blocks

    basic.pause(750)

    moveResult = moveblockDown()
    if moveResult == False:
        coutFrame = 0
        #Si el movimiento no es posible, el bloque se mantiene en la misma posición
        tetris[y_position][x_position] = max(block[0][0], tetris[y_position][x_position])
        tetris[y_position][x_position + 1] = max(block[0][1], tetris[y_position][x_position + 1])
        tetris[y_position + 1][x_position] = max(block[1][0], tetris[y_position + 1][x_position])
        tetris[y_position + 1][x_position + 1] = max(block[1][1], tetris[y_position + 1][x_position + 1])

        if checkCompletedLines() == False and y_position == 0:
            # El bloque ha alcanzado el top del display - Game Over
            gameOn = False
            #Fin del juego
            pause(2000)
            game.game_over()
            basic.show_string("Game Over")
            basic.show_string("Score: ")
            basic.show_string(str(score))
        else:
            #Selecciona un nuevo bloque aleatoriamente
            x_position = 3
            y_position = 0
            # ----------------------------------------------
            block = blocks[randint(0, blocks.length - 1)]
            changeLedState(True)

basic.forever(on_forever)
