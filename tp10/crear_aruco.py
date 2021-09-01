# Este script es utilizado para la creacion de Arucos
# ----------------------------------------------------
# Se genera un archivo .png con el id correspondiente
#
# Se deben configurar los siguientes parametros
# antes de ejectutar:
# size:  tamaño del Aruco en pixeles
# borde: cantidad de bloques negros de borde ( >=1)
# ----------------------------------------------------
import os
import shutil
import cv2 as cv
import numpy as np
# ----------------------------------------------------
dir = 'tmp'
if(os.path.exists(dir)):
    shutil.rmtree(dir)
if(not os.path.exists(dir)):
    os.mkdir(dir)
output_file = '{}/aruco_id{:03}.png'
# ----------------------------------------------------
title_img = 'AruCo'
id = 0                        # Id del marcador Aruco
borde = 1                     # Cantidad de bloques negros de borde
size = 220                    # tamaño del marcador en pixeles
dicc = cv.aruco.DICT_4X4_250
#dicc = cv.aruco.DICT_6X6_250

img = np.zeros((size, size), dtype=np.uint8)
# ----------------------------------------------------
#  Cargar el diccionario predefinido...
diccionario = cv.aruco.Dictionary_get(dicc)
# **************************************************
# Funcion: Generar marcador AruCo.
# **************************************************
def gen_aruco():
    global img, id
    img = cv.aruco.drawMarker(diccionario, id, size, img, borde)
    print('AruCo id: {0}'.format(id))
# **************************************************
# Funcion para guargar el AruCo generado.
# **************************************************
def guardar(imagen):
    cv.imwrite(output_file.format(dir, id), imagen)
# ***************************************************
# Mensajede presentacion - Indicaciones
# ***************************************************
def mjeInincio():
    print('------------------------------------------------')
    print('         *** Generador AruCo ***')
    print('------------------------------------------------')
    print('[W] Siguiente')
    print('[S] Anterior')
    print('[E] Ingrese Id por teclado')
    print('[G] Guardar Aruco')
    print('[H] Help')
    print('[Q] Salir')
# ***************************************************
mjeInincio()
gen_aruco()

while (True):

    #cv.namedWindow(title_img + str(id))
    cv.imshow(title_img, img)

    k = cv.waitKey(20) & 0xFF
    if k == ord('g') or k == ord('G'):           # guardar la imagen generada
        guardar(img)
        print('Imagen generada id: {0}'.format(id))

    if k == ord('w') or k == ord('W'):           # incrementar id
        if(id == 249):
            id = 0
        else:
            id += 1
        gen_aruco()

    if k == ord('s') or k == ord('S'):           # Decrementar id
        if(id == 0):
            id = 249
        else:
            id -= 1
        gen_aruco()

    if k == ord('e') or k == ord('E'):            # Ingresa Id por teclado
        #print('Ingrese el id: ')
        id = int(input('Ingrese el id: '))
        gen_aruco()

    if k == ord('h') or k == ord('H'):            # Mostar el HELP
        mjeInincio()

    if k == ord('q') or k == ord('Q'):            # finalizar el script
        print('Script finalizado correctamente')
        break
#----------------------------------------------------
cv.destroyAllWindows()