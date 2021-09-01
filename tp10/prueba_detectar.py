# Deteccion con Aruco
# ----------------------------------------------------------
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
# **************************************************
# Funcion para la busqueda de los marcadores
# **************************************************
def findArucos(img, draw=True):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    arucoDic = aruco.Dictionary_get(cv.aruco.DICT_4X4_250)              # cargo el diccionario
    arucoPar = aruco.DetectorParameters_create()                        # Creo el Detector
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDic, parameters=arucoPar)
    if draw:
        img = aruco.drawDetectedMarkers(img, corners , ids)
    return [corners, ids]
# **************************************************

# **************************************************
cap = cv.VideoCapture(0)
fps = cap.get(cv.CAP_PROP_FPS)
while (True):
    ret, imagen = cap.read()
    marcadores = findArucos(imagen)
    if marcadores[1] is not None:               # ids
        print("")
        print("Esquinas: {}".format(marcadores[0]))
        print("Id: {}".format(marcadores[1]))

    cv.imshow("Deteccion", imagen)
    key = cv.waitKey(int(fps))
    if key == ord('q') or key == ord('Q'):
        break;

cap.release()
cv.destroyAllWindows()
