#! /usr/bin/env python
# -*- coding: utf-8 -*-
#****************************************************************************************
#                       TP9: Medición de objetos
#****************************************************************************************
#
# En base a las medidas de la puerta de un mueble, el programa permite tomar medidas 
# siempre tomadas en el mismo plano.
#
# 'g' guarda la imagen con las mediciones actuales
# 'r' restaura la imagen (con la transf. de perspectiva aplicada, lista para las mediciones)
# 'o' permite mostrar la imagen original tomada en perspectiva
# 'q' finaliza el script
#****************************************************************************************
# El script lee la imagen 'entrada.jpg'
#****************************************************************************************

import os
import shutil
import cv2
import numpy as np
from math import sqrt

#****************************************************************************************
#                           Mediciones Reales
#
# Ancho de Puerta   -> 29,6cm 
# Alto de Puerta    -> 53,0cm
# Canto de la madera->  1,8cm
# Ancho de la imagen rectificada 188cm
# Ancho de la imagen rectificada 53.6cm
# Relacion de aspecto usada W:800, H:600
#----------------------------------------------------
# esquinas = [[26,139],[781,231],[794,415],[10,509]]
cm_px_x = 0.235             # cm_px_x = 188/800
cm_px_y = 0.09              # cm_px_y = 53.6/600
#----------------------------------------------------
dir = 'tmp'                 # preparo el directorio de salida para guardar las imagenes
if(os.path.exists(dir)):
    shutil.rmtree(dir)
if(not os.path.exists(dir)):
    os.mkdir(dir)
output_file = '{}/{:03}.png'
cont = 1
#----------------------------------------------------

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False         # True si el mouse es presionado
ptos = []               # lista de puntos seleccionados para la medicion
title_img = 'Imagen Rectificada'
title_img_orig = 'Imagen original tomada en perspectiva'
img_entrada = 'entrada.jpg'

esquinas = [[26,139],[781,231],[794,415],[10,509]]

#**********************************************************************
# Funcion para guardar las mediciones de la imagen.
#**********************************************************************
def guardar(imagen):
    global cont
    cv2.imwrite(output_file.format(dir,cont),imagen)
    print("imagen guardada:", output_file.format(dir,cont))
    cont+=1

#**********************************************************************
# Funcion para rectificar la imgen original.
#**********************************************************************
def t_perspectiva(imagen):

    pts1 = np.float32([esquinas])
    print('T. Homografia -> p1: {0}, p2: {1}, p3: {2}, p4: {3}'
                  .format(esquinas[0], esquinas[1], esquinas[2], esquinas[3]))

    p_out = np.float32([[0,0],[ancho,0],[ancho,alto],[0,alto]])
                
    H = cv2.getPerspectiveTransform(pts1, p_out)
    tp = cv2.warpPerspective(imagen, H, (ancho, alto))
    return tp

#**********************************************************************
# Funcion convertir de pixeles a metros.
#**********************************************************************
#
# Primero debo encontrar la hipotenusa del triangulo formado por el
# delta en X y el delta en Y, esa sera la distancia a convertir  de
# pixeles a metros.
# Los incrementos pueden ser negativos pero al elevarlos al cuadrado
# no es necesario controlar esta condicion para que las mediciones
# sean siempre positivas
#**********************************************************************
def px_to_m(pi,pf):

    cx = pf[0] - pi[0]	     
    cy = pf[1] - pi[1]

    cmx = cx*cm_px_x/100
    cmy = cy*cm_px_y/100
    hip = sqrt(cmx**2 + cmy**2)
        
    hip = round(hip, 3)	
    print('cx: {0}, cy: {1}, cmx: {2}, cmy: {3}, -> {4}m'
          .format(cx, cy, cmx, cmy, hip))
    return str(hip)
    
#**********************************************************************
# Funcion de callback para eventos del mouse.
#**********************************************************************
def marcar_puntos(event, x, y, flags, param):
    global drawing, ptos
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        drawing = True
        ptos.append([x,y])
        if (len(ptos)==2):   
            print("")
            print("Puntos: ", ptos)            
            cv2.line(img_marcada, ptos[0],ptos[1], green)
            medicion = px_to_m(ptos[0],ptos[1])
            cv2.putText( img_marcada , medicion+'m', (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, green, 1 , cv2.LINE_AA)
            # actualizo la imagen de base
            img_rectificada[:] = img_marcada[:]
            drawing = False
            ptos.clear()
        
    elif (event == cv2.EVENT_MOUSEMOVE):
        if (drawing is True):            
            img_marcada[:] = img_rectificada[:]
            cv2.line(img_marcada, ptos[0], (x,y), green)            
            
#**********************************************************************
# Inicio del script
#**********************************************************************
print("TP N9")
print("Menu de opciones:")
print("'g' guarda la imagen con las mediciones actuales.")
print("'r' restaura la imagen.")
print("'o' mostrar la imagen original tomada en perspectiva.")
print("'q' finaliza el script.")
print("")
            
img = cv2.imread(img_entrada, 1)

alto,ancho = img.shape[:2]
print('Imagen Original-> H: {0}, W: {1}, ratio: {2}'
      .format(alto,ancho,(alto/ancho)))

img_rectificada = t_perspectiva(img)
copia_rectif = img_rectificada.copy()	        # hago una copia para poder restaurarla
img_marcada = img_rectificada.copy()	         
cv2.imwrite('imagen rectificada.png', img_rectificada)

cv2.namedWindow(title_img)
cv2.setMouseCallback(title_img, marcar_puntos)

while(1):
    cv2.imshow(title_img, img_marcada)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('g'):      # guarda la imagen con las selecciones actuales
        guardar(img_marcada)        

    if k == ord('o'):      # permite mostrar la imagen original tomada en perspectiva
        print('Imagen Original...')
        cv2.imshow(title_img_orig, img)
                
    if k == ord('r'):      # restaurar la imagen rectificada
        img_rectificada[:] = copia_rectif[:]
        img_marcada[:] = copia_rectif[:]
        cv2.imshow(title_img, img_marcada)
        print('Imagen restaurada')
        
    if k == ord('q'):      # finalizar el script
        print('Script finalizado correctamente')
        break
    
#**************************************************

cv2.destroyAllWindows()
