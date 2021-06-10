#*************************
# TP1: adivinador.py
#*************************

import random
#*************************
#*** Funcion: adivina ****
#*************************
def adivina(intentos):
    numero = random.randint(0, 100)
#    print('debug',str(numero)) # Para poder probar la funcion a modo de debug

    for i in range(0, intentos):
        apuesta = int(input('Intente adivinar: '))
        if apuesta == numero:
            print('Correcto!, Ud adivinó en el intento Nº{}'.format(i+1))
            break
        elif apuesta < numero:
            print('No, es mas grande')
        else:
            print('No, es mas chico')
    else:
        print('Lo siento, alcanzó el máximo de intentos sin adivinar')
#*** Fin funcion: adivina***
#***************************
print('Debe adivinar un número entre 0 y 100 que se genera aleatoriamente')
veces = int(input('Ingrese la cantidad de intentos: '))

adivina(veces)

