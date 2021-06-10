#! /usr/bin/env python
# -*- coding: utf-8 -*-
#**************************************************
#           TP4: Manipulacion de imagenes
#**************************************************
# 'g' guardar la porción de la imagen seleccionada
# 'r' restaurar la imagen original 
# 'q' finaliza el script
#
# El script lee la imagen 'logo.png'
# luego guarda la seleccion como 'recorte.png'
#**************************************************
import cv2
import numpy as np

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False         # True si mouse el mouse es presionado
xybutton_down = -1, -1
xybutton_up = -1, -1
title_img = 'Logo OpenCV en Colores'

img = cv2.imread('logo.png',1)
alto,ancho,canales = img.shape
print('alto: {0}, ancho: {1}, canales: {2}'.format(alto,ancho,canales))

img2 = np.zeros((alto, ancho, 3), np.uint8)
# hago una copia de la original para restaurar 
img2[:] = img[:]                            

#*******************************************
# Funcion para guardar el recorte de la img.
# Calculo el tamaño de la nueva imagen y
# luego se guarda como 'recorte.png'
#*******************************************
def guardar():
    # Evito valores negativos al hacer al soltar el click
    #fuera de la ventana
    xi = xybutton_down[0] if xybutton_down[0]>0 else 0
    yi = xybutton_down[1] if xybutton_down[1]>0 else 0
    xf = xybutton_up[0] if xybutton_up[0]>0 else 0 
    yf = xybutton_up[1] if xybutton_up[1]>0 else 0
    if(xf>xi):
        x = xf-xi
        anchoi = xi
        anchof = xf
    else:
        x = xi-xf
        anchoi = xf
        anchof = xi
    if(yf>yi):
        y = yf-yi
        altoi = yi
        altof = yf
    else:
        y = yi-yf
        altoi = yf
        altof = yi
    img3 = np.zeros((y, x, 3), np.uint8)
    print('tamaño seleccion -> W: {0}, H: {1}'.format(x, y))
    img3 = img2[altoi:altof, anchoi:anchof]
    cv2.imwrite('recorte.png',img3)

#*******************************************
# Funcion de callback para eventos del mouse
#*******************************************
def draw_cut(event, x, y, flags, param):
    global xybutton_down, xybutton_up, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xybutton_down = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img[:] = img2[:] 
            cv2.imshow(title_img, img)
            cv2.rectangle(img, xybutton_down, (x, y), green, 1)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing is True:
            xybutton_up = x, y
            print(xybutton_down, xybutton_up)
            img[:] = img2[:]
            cv2.imshow(title_img, img)
            cv2.rectangle(img, xybutton_down, (x, y), blue, 2)            
            drawing = False

#*******************************************
cv2.imshow(title_img,img)
cv2.setMouseCallback(title_img, draw_cut)

while(1):
    cv2.imshow(title_img, img)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('g'):           # guardar la porción de la imagen seleccionada
        guardar()        
        
    if k == ord('r'):           # restaurar la imagen original        
        img[:] = img2[:] 
        cv2.imshow(title_img,img)
        print('Imagen restaurada')
        
    if k == ord('q'):           # finalizar el script
        print('Script finalizado correctamente')
        break

cv2.destroyAllWindows()
