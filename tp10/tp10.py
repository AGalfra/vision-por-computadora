# ----------------------------------------------------------------------------------
# Alumno: Alejandro Galfrascoli
# Legajo: 43029
# UTN - FRC
# Vision por computadora
# TP N10: ARUCO -  Practico libre
# DESCRIPCION:
# El script utiliza 4 marcadores aruco (Id: 1, 11, 21 y 31) para ubicar las cuatro
# esquinas de una tabla, sobre la que se coloca la imagen definida como mascara
# por medio de una transformación de homografia.
#
# Se puede correr el mismo con el video de muestra 'video_base.mp4' o configurando
# camara = 1, la captura se realiza a traves de la camara (Requiere de los 4 arucos).
#
# Tambien es posible generar un archivo de salida poniendo grabar = 1.
#
# Colocando debug = 1 muestra las imagenes aux de deteccion de Arucos y Homografia.
#
# La variable fpsSD se utiliza para darle estabilidad a la imagen, ya que en los
# momentos en que se detecten menos de los 4 arucos pero la cantidad de FPS es
# menor que MaxFPS (definido en 5) se sigue mostrando la homografia anterior.
# con esto se evitan parpadeos de la homografia, y en 5 FPS el cambio es minimo.
# ----------------------------------------------------------------------------------
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
# ***********************************************************************************
# Definicion de variables
# -----------------------------------------------------------------------------------
mascara = 'picada.jpg'          # Video de mascara.
videoEntrada = 'video_base.mp4' # video base para demostracion.
video_out = 'videoSalida.avi'   # Nombre del video generado.
MaxFPS = 5                      # Umbral de frames sin detectar 4 Arucos.
camara = 0                      # 1: Captura desde la camara, 0: desde archivo.
                                # Habilitar grabacion solo si captura desde la camara
grabar = 0                      # poner en 0 para no generar archivo de salida
debug = 0                       # muestra las imagenes auxiliares
# ***********************************************************************************
# Funcion para la busqueda de los marcadores
# -----------------------------------------------------------------------------------
def findArucos(img, draw=True):

    #imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    arucoDic = aruco.Dictionary_get(aruco.DICT_4X4_50)              # cargo el diccionario
    arucoPar = aruco.DetectorParameters_create()                    # Creo el Detector
    corners, ids, rejected = aruco.detectMarkers(img, arucoDic, parameters=arucoPar)
    if draw:
        if debug:
            img = aruco.drawDetectedMarkers(img, corners, ids)
            cv.imshow('Salida findArucos()', img)
        else:
            img = aruco.drawDetectedMarkers(img, corners)
    return [corners, ids]
# ***********************************************************************************
# Funcion para la Transformacion de Homografia
# y sumar la imagen con la de la camara o la leida desde el archivo
#     upL -> Aruco Id: 1
#     upR -> Aruco Id: 11
#     dwR -> Aruco Id: 21
#     dwL -> Aruco Id: 31
# -----------------------------------------------------------------------------------
def acoplar(esquinas, id, img, mask):
    esq = [-1,-1,-1,-1]
    h, w = mask.shape[:2]
    ho, wo = img.shape[:2]
    for i in range(4):
        esq[i] = int(id[i])

    if esq.index(1) is not None:
        aruco01 = esq.index(1)
    else:
        return img
    if esq.index(11) is not None:
        aruco11 = esq.index(11)
    else:
        return img
    if esq.index(21) is not None:
        aruco21 = esq.index(21)
    else:
        return img
    if esq.index(31) is not None:
        aruco31 = esq.index(31)
    else:
        return img

    upL = esquinas[aruco01][0][0][0], esquinas[aruco01][0][0][1]
    upR = esquinas[aruco11][0][0][0], esquinas[aruco11][0][0][1]
    dwR = esquinas[aruco21][0][0][0], esquinas[aruco21][0][0][1]
    dwL = esquinas[aruco31][0][0][0], esquinas[aruco31][0][0][1]

    pts1 = np.array([upL, upR, dwR, dwL])                   # puntos definidos por las esquinas de los AruCos
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])     # esquinas de la imagen de mascara
    #H, _m = cv.findHomography(pts2, pts1)
    H = cv.getPerspectiveTransform(pts2, pts1)
    img_h = cv.warpPerspective(mask, H, (wo, ho))
    if debug:
        cv.imshow('Homografia', img_h)
    cv.fillConvexPoly(img, pts1.astype(int), (0, 0, 0))
    img_compuesta = img + img_h
    return img_compuesta

# ***********************************************************************************
print('')
if camara:
    print('accediendo a la camara')
    cap = cv.VideoCapture(0)
else:
    print('leyendo el archivo: '+ videoEntrada)
    cap = cv.VideoCapture(videoEntrada)

fps = cap.get(cv.CAP_PROP_FPS)
mask = cv.imread(mascara)

if grabar:
    salida = cv.VideoWriter(video_out, cv.VideoWriter_fourcc(*'XVID'), fps, (640,480))

fpsSD = 0       # cantidad de frames sin detectar 4 Arucos

while cap.isOpened():
    ret, imagen = cap.read()
    if ret:
        marcadores = findArucos(imagen)
        esquinas = marcadores[0]
        ids = marcadores[1]
        fpsSD += 1

        if len(esquinas) == 4:
            print("")
            print("Id: {}".format(ids))
            if debug:
                print("Esquinas: {}".format(esquinas))
            imagen = acoplar(esquinas, ids, imagen, mask)
            cv.imshow("combinadas", imagen)
            fpsSD = 0

        if grabar:
            salida.write(imagen)

        if fpsSD >= MaxFPS:       # si pasaron MaxFPS frames sin deteccion de 4 arcucos debo mostrar imagen cruda
            cv.imshow("combinadas", imagen)

    else:
        break       # Salida por finalizacion de lectura de archivo

    k = cv.waitKey(int(fps)) & 0xFF
    if k == ord('q') or k == ord('Q'):
        break
# ----------------------------------------------------
if grabar:
    salida.release()
cap.release()
cv.destroyAllWindows()
