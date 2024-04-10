function changeLedState(NewState: boolean) {
    
    
    
    
    if (NewState === true) {
        // Muestra el bloque actual
        if (x_position > 0) {
            led.plotBrightness(x_position - 1, y_position, Math.max(block[0][0], tetris[y_position][x_position]))
        }
        
        if (x_position < 5) {
            led.plotBrightness(x_position - 1 + 1, y_position, Math.max(block[0][1], tetris[y_position][x_position + 1]))
        }
        
        if (x_position > 0 && y_position < 4) {
            led.plotBrightness(x_position - 1, y_position + 1, Math.max(block[1][0], tetris[y_position + 1][x_position]))
        }
        
        if (x_position < 5 && y_position < 4) {
            led.plotBrightness(x_position - 1 + 1, y_position + 1, Math.max(block[1][1], tetris[y_position + 1][x_position + 1]))
        }
        
    } else {
        // Oculta el bloque actual
        if (x_position > 0) {
            led.plotBrightness(x_position - 1, y_position, tetris[y_position][x_position])
        }
        
        if (x_position < 5) {
            led.plotBrightness(x_position - 1 + 1, y_position, tetris[y_position][x_position + 1])
        }
        
        if (x_position > 0 && y_position < 4) {
            led.plotBrightness(x_position - 1, y_position + 1, tetris[y_position + 1][x_position])
        }
        
        if (x_position < 5 && y_position < 4) {
            led.plotBrightness(x_position - 1 + 1, y_position + 1, tetris[y_position + 1][x_position + 1])
        }
        
    }
    
    
}

// Aplica la rotación a la posición del bloque actual
// Mueve el bloque en el eje X (Izquierda y Derecha) y en el eje Y (abajo)
function moveBlock(x_move: number, y_move: number): boolean {
    
    let move = false
    // Verifica que el movimiento es posible
    if (x_move == -1 && x_position > 0) {
        if (!(tetris[y_position][x_position - 1] > 0 && block[0][0] > 0 || tetris[y_position][x_position + 1 - 1] > 0 && block[0][1] > 0 || tetris[y_position + 1][x_position - 1] > 0 && block[1][0] > 0 || tetris[y_position + 1][x_position + 1 - 1] > 0 && block[1][1] > 0)) {
            move = true
        }
        
    } else if (x_move == 1 && x_position < 5) {
        if (!(tetris[y_position][x_position + 1] > 0 && block[0][0] > 0 || tetris[y_position][x_position + 1 + 1] > 0 && block[0][1] > 0 || tetris[y_position + 1][x_position + 1] > 0 && block[1][0] > 0 || tetris[y_position + 1][x_position + 1 + 1] > 0 && block[1][1] > 0)) {
            move = true
        }
        
    } else if (y_move == 1 && y_position < 4) {
        if (!(tetris[y_position + 1][x_position] > 0 && block[0][0] > 0 || tetris[y_position + 1][x_position + 1] > 0 && block[0][1] > 0 || tetris[y_position + 1 + 1][x_position] > 0 && block[1][0] > 0 || tetris[y_position + 1 + 1][x_position + 1] > 0 && block[1][1] > 0)) {
            move = true
        }
        
    }
    
    // Si el movimiento es posible, se puede actualizar los ejes X e Y del bloque
    if (move) {
        changeLedState(false)
        // hideblock()
        x_position += x_move
        y_position += y_move
        changeLedState(true)
    }
    
    // Devuelve True o False si el movimiento del bloque es posible
    return move
}

function moveblockDown(): boolean {
    let x_move = 0
    let y_move = 1
    return moveBlock(x_move, y_move)
}

// Comprueba las lineas si alguna esta completa
function checkCompletedLines(): boolean {
    let i: number;
    let j: number;
    
    
    
    
    
    let removeLine = false
    // Comprueba cada linea de una en una 
    for (i = 0; i < 5; i++) {
        // Si una linea ha sido completada entonces esta deberá de ser eliminada y la puntuación aumentada
        if (tetris[i][1] + tetris[i][2] + tetris[i][3] + tetris[i][4] + tetris[i][5] == on_led_value * 5) {
            removeLine = true
            // Incrementa la puntuación
            score += winingScore
            // Elimina la linea y hace que las superiores caigan
            for (j = i; j > 0; j += -1) {
                tetris[j] = tetris[j - 1]
            }
            tetris[0] = [1, 0, 0, 0, 0, 0, 1]
        }
        
    }
    if (removeLine) {
        // Actualiza el display LED
        for (i = 0; i < 5; i++) {
            for (j = 0; j < 5; j++) {
                led.plotBrightness(i, j, tetris[j][i + 1])
            }
        }
    }
    
    return removeLine
}

function play_music() {
    music.startMelody(music.builtInMelody(Melodies.Dadadadum))
}

function init_game() {
    // Mensaje de inicio
    basic.showNumber(3)
    basic.showNumber(2)
    basic.showNumber(1)
    basic.showString("GO")
    // Eventos --------------------------------------------
    // Evento del boton táctil
    input.onLogoEvent(TouchButtonEvent.Pressed, function rotateblock() {
        let block00: number;
        
        
        
        
        // Comprueba si la rotación es posible
        if (!(tetris[y_position][x_position] > 0 && block[0][0] > 0 || tetris[y_position + 1][x_position] > 0 && block[1][0] > 0 || tetris[y_position][x_position + 1] > 0 && block[0][1] > 0 || tetris[y_position + 1][x_position + 1] > 0 && block[1][1] > 0)) {
            // Oculta el bloque para aplicar la rotación
            // hideblock()
            changeLedState(false)
            // Aplica la rotación
            block00 = block[0][0]
            block[0][0] = block[1][0]
            block[1][0] = block[1][1]
            block[1][1] = block[0][1]
            block[0][1] = block00
            // showblock()
            changeLedState(true)
        }
        
    })
    // Evento de los botones
    input.onButtonPressed(Button.A, function moveblockLeft() {
        let x_move = -1
        let y_move = 0
        moveBlock(x_move, y_move)
    })
    input.onButtonPressed(Button.B, function moveblockRight(): boolean {
        let x_move = 1
        let y_move = 0
        return moveBlock(x_move, y_move)
    })
    // Micrófono
    // play_music()
    // Giroscopio
    input.onGesture(Gesture.Shake, function on_gesture_shake() {
        control.reset()
        
    })
}

//  --------------------------------------------
// Starteo de programa -------------------------------------------->>>>>>>>>>>>
init_game()
// Intensidad máxima del LED
let on_led_value = 255
// Puntuacion que se añade cuando se complete una linea
let winingScore = 10
// Crea una matriz del tetris
let tetris = [[1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]
// Crea las posibilidades del generamiento de bloques
let blocks = [[[on_led_value, on_led_value], [on_led_value, 0]], [[on_led_value, on_led_value], [0, on_led_value]], [[on_led_value, on_led_value], [on_led_value, on_led_value]], [[on_led_value, on_led_value], [0, 0]]]
// Selecciona el bloque aleatoriamente
let block = blocks[randint(0, blocks.length - 1)]
// Posicion inicial del primer bloque
let x_position = 2
let y_position = 0
let coutFrame = 0
let gameOn = true
let score = 0
changeLedState(true)
// Bucle del programa principal - itera cada 50ms
basic.forever(function on_forever() {
    let coutFrame: number;
    
    
    
    
    
    
    basic.pause(750)
    let moveResult = moveblockDown()
    if (moveResult == false) {
        coutFrame = 0
        // Si el movimiento no es posible, el bloque se mantiene en la misma posición
        tetris[y_position][x_position] = Math.max(block[0][0], tetris[y_position][x_position])
        tetris[y_position][x_position + 1] = Math.max(block[0][1], tetris[y_position][x_position + 1])
        tetris[y_position + 1][x_position] = Math.max(block[1][0], tetris[y_position + 1][x_position])
        tetris[y_position + 1][x_position + 1] = Math.max(block[1][1], tetris[y_position + 1][x_position + 1])
        if (checkCompletedLines() == false && y_position == 0) {
            //  El bloque ha alcanzado el top del display - Game Over
            gameOn = false
            // Fin del juego
            pause(2000)
            game.gameOver()
            basic.showString("Game Over")
            basic.showString("Score: ")
            basic.showString("" + score)
        } else {
            // Selecciona un nuevo bloque aleatoriamente
            x_position = 3
            y_position = 0
            //  ----------------------------------------------
            block = blocks[randint(0, blocks.length - 1)]
            changeLedState(true)
        }
        
    }
    
})
