import os, time, random


class ListaDeJuego(list):
    '''Listas modificadas para acoplarse a un tablero 3x3.
    
    Estas listas modifican el inicio de la inexacion, empezandola en 1,
    ademas, bloquean el cambio de valor al existir un valor diferente a "_",
    exceptuando cuando estos valores terminan con una "p" eliminando esta al
    antes de cambiar de valor.'''

    def __init__(self, lista):
        self.lista = list(lista)

    def __getitem__(self, index):
        if 0 < index < 4:
            index -= 1
            return self.lista[index]
        else:
            raise IndexError
        
    def __setitem__(self, index, valor):
        if 0 < index < 4:
            index -= 1
            if valor.find('p') == -1 or valor.find('p') == -1:
                if self.lista[index] != '_':
                    raise OccupedSpaceError
                else:
                    self.lista[index] = valor
            else:
                self.lista[index] = valor[:len(valor) - 1]
        else:
            raise IndexError

    def __str__(self):
        return "{}".format(self.lista)

    def __repr__(self):
        return "{}".format(self.lista)

class OccupedSpaceError(Exception):
    '''Una excepcion para poder denegar el cambio de un valor que sea
    diferente a "_".'''

    pass

    
def limpiar():
    '''Funcion que es utilizada para limpiar de pantalla.
    
    En teoria debe de lograr borrar pantalla sin importar si es un SO de Windows o de Linux.'''

    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

def tablero(color):
    '''Imprime un tablero 3x3, para el juego Ta Te Ti.
    
    La funcion imprime el tablero sin importar si este esta vacio o lleno, cambia 
    el color del tablero exceptuando los espacios de juego, aunque tambien imprime
    los ultimos.'''

    global juego
    print(color + "   1 2 3\n")
    for i in range(1, 4):
        print(i, "", end="")
        for j in range(1, 4):
            print('|' + juego[i][j], end=color)
        print('|\n')
    print('\033[0;37;40m', end="")

def winner_winner_chicken_dinner(ia):
    '''La funcion determina si hay un ganador o si hay un empate.
    
    Se basa en la busqueda de una secuencia de 3 "○" o de 3 "x" en las lineas
    verticales, horizontales y diagonales, si no encuetra estas secuencias procede a 
    buscar si existe un empate buscan si hay algun "_" todavia, si encuentra alguna de
    las secuencias anteriores devolvera un "False" para terminar el ciclo de la funcion
    "jugando" y cambiara el color de la secuencia y el tablero en caso de un ganador,
    o en el caso de un empate solamente cambia el color del tablero, de no encontrar
    ninguna coincidencia devolvera "True" para mantener el ciclo en "jugando".'''
    limpiar()

    global juego
    vertical = ""
    horizontal = ""
    diagonal = ""
    jugador = ""
    if ia == '○':
        jugador = 'x'
    elif ia == 'x':
        jugador = '○'

    for i in range(1, 4):
        diagonal += juego[i][i][-1]
        for j in range(1, 4):
            vertical += juego[i][j][-1]
            horizontal += juego[j][i][-1]
        vertical += " "
        horizontal += " "

    diagonal += " "
    for i in range(1, 4):
            diagonal += juego[i][abs(i - 4)][-1]

    lineas = [vertical, horizontal, diagonal]
    busqueda_de_empate = vertical + horizontal + diagonal

    for i in range(1, 4):
        if lineas[i - 1].find(jugador * 3) == 0 or lineas[i - 1].find(ia * 3) == 0:
            index = 1

        elif lineas[i - 1].find(jugador * 3) == 4 or lineas[i - 1].find(ia * 3) == 4:
            index = 2

        elif lineas[i - 1].find(jugador * 3) == 8 or lineas[i - 1].find(ia * 3) == 8:
            index = 3

        if lineas[i - 1].find(jugador * 3) != -1:
            for j in range(1, 4):
                if i == 1:
                    juego[index][j] = '\033[1;32;40m' + jugador + 'p'

                elif i == 2:
                    juego[j][index] = '\033[1;32;40m' + jugador + 'p'

                elif i == 3:
                    if index == 1:
                        juego[j][j] = '\033[1;32;40m' + jugador + 'p'
                    elif index == 2:
                        juego[j][abs(j - 4)] = '\033[1;32;40m' + jugador + 'p'

            tablero('\033[1;32;40m')
            print("¡¡Felicidades, ganaste!!")
            time.sleep(4)
            return False

        elif lineas[i - 1].find(ia * 3) != -1:
            for j in range(1, 4):
                if i == 1:
                    juego[index][j] = '\033[1;36;40m' + ia + 'p'

                elif i == 2:
                    juego[j][index] = '\033[1;36;40m' + ia + 'p'

                elif i == 3:
                    if index == 1:
                        juego[j][j] = '\033[1;36;40m' + ia + 'p'
                    elif index == 2:
                        juego[j][abs(j - 4)] = '\033[1;36;40m' + ia + 'p'

            tablero('\033[1;31;40m')
            print("¡La computadora gano!")
            time.sleep(4)
            return False
    
    if busqueda_de_empate.find('_') == -1:
        tablero('\033[1;34;40m')
        print("¡Hubo un empate!")
        time.sleep(4)
        return False

    return True

def supuesta_ia(entrada):
    '''Simula un juego contra el computador.
    
    Solamente devuelve dos numeros aleatorios y si estos devuelven error vuelve a intentar,
    asi hasta que encuentre una posicion vacia.'''
    
    while True:
        try:
            juego[random.randint(1, 3)][random.randint(1, 3)] = '\033[1;31;40m' + entrada
            break
        except:
            continue

def jugando(entrada, ia):
    '''"jugando" pregunta la posicion en la cual desea jugar el usuario.
    
    La funcion esta hecha de dos ciclos uno para mantener la continua entrada de datos hasta
    que haya un ganador o un empate, el segundo para mantener las solicitudes de las cooredenadas
    en caso de ingresarse fuera de los limites del tablero o en una posicion ya ocupada. Ademas,
    comprueba despues de cada movimiento si existe un ganador o un empate.'''

    blanco = '\033[0;37;40m'
    color = ""
    hasta_ganar_empatar = True
    if entrada == entradas['2']:
        supuesta_ia(ia)

    while hasta_ganar_empatar:
        limpiar()
        print("¿En que espacio desea colocar " + entrada + "\n")
        tablero(blanco)

        while True:
            posicion = []
            try:
                print("Fila:\t\t", end="")
                posicion.append(int(input()))
                print("Columna:\t", end="")
                posicion.append(int(input()))
                juego[posicion[0]][posicion[1]] = '\033[1;33;40m' + entrada[-12]
                limpiar()
                tablero(blanco)
                time.sleep(1)
                hasta_ganar_empatar = winner_winner_chicken_dinner(ia)

                if not hasta_ganar_empatar:
                    break

                supuesta_ia(ia)
                break

            except IndexError:
                print("\nSolo puede ingresar numeros del 1 al 3, incluidos ambos.")
                continue

            except OccupedSpaceError:
                print("\nEl espacio escogido ya fue ocupado con anterioridad, escoja un espacio libre (uno de los que tienen '_')")
                continue

        if not hasta_ganar_empatar:
            break

        hasta_ganar_empatar = winner_winner_chicken_dinner(ia)
    limpiar()
        

entradas = {'1':"\033[0;37;40mla '\033[1;33;40mx\033[0;37;40m'", '2':"\033[0;37;40mel '\033[1;33;40m○\033[0;37;40m'", }

# Ciclo principal del juego
while True:
    juego = ListaDeJuego([ListaDeJuego(['_' for i in range(3)]) for j in range(3)])
    ciclo_respuesta = True
    limpiar()
    print("\033[0;37;40m\n¿Desea jugar con \033[0;36;40m1. 'x'\033[0;37;40m o con \033[0;36;40m2. '○'\033[0;37;40m?")
    print("(Las 'x' empiezan el juego, responda con '1' o '2'):\t", end="")

    while ciclo_respuesta:
        respuesta = input()

        if respuesta == "1" or respuesta == "2":
            ciclo_respuesta = False
            limpiar()
            if respuesta == "1":
                jugando(entradas["1"], "○")
            elif respuesta == "2":
                jugando(entradas["2"], "x")
            break
            
        else:
            print("Por favor, responda con \033[0;36;40m'1'\033[0;37;40m o con \033[0;36;40m'2'\t", end="")
    limpiar()
    print("¿Desea seguir jugando? ('Si', 'No'):", end="\t")
    if input().lower() == "no":
        break
