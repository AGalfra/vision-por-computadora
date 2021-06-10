#! /usr/bin/env python
# -*- coding: utf-8 -*-
#**************************************************
#           TP3: Propiedades de Video
#**************************************************
# se abre un archivo de video que es pasado como
# argumento, lo muestra en grises  y genera como
# salida otro archivo llamado 'output.avi'.
#
# El script obtiene el framesize y fps utilizando
# funciones de las OpenCV
#
#************************************************** 
import sys
import cv2

if (len(sys.argv)>1):
    filename = sys.argv[1]
    print('Archivo: ' + filename)
else:
    print('Pasar un nombre de archivo como argumento')
    sys.exit(0)

cap = cv2.VideoCapture(filename)
# Capturo de fps, alto y ancho de las imagenes
fps = cap.get(cv2.CAP_PROP_FPS)
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print('fps: {0}, w: {1}, h: {2}'.format(fps, w, h))

framesize = (w,h)
#Especifico formato de video
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter('output.avi', fourcc, fps, framesize)
 
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video en Grises', gray)
        out.write(frame)
        if cv2.waitKey(int(fps)) & 0xFF == ord('q'):
            break
    else:      
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()
