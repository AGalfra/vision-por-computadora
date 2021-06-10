#! /usr/bin/env python
# -*- coding: utf-8 -*-
#**************************************************
#           TP2: Umbralizado binario
#**************************************************
# Se internta realizar un umbralizado sencillo sin
# la utilizacion de las funciones de la OpenCV
#**************************************************
import cv2
img=cv2.imread('hoja.png',0)
alto,ancho=img.shape
print('alto: {0}, ancho: {1}'.format(alto,ancho))
umbral = 200
for y in range(0,alto):
        for x in range(0,ancho):
                if img[x,y] < umbral:
                        img[x,y]=0
                else:
                        img[x,y]=255

cv2.imwrite('umbralizado.png',img)

cv2.imshow('Imagen Umbralizada', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
