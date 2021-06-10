#! /usr/bin/env python
# -*- coding: utf-8 -*-
#**************************************************
#           TP8: Rectificando imágenes
#**************************************************
# 'g' guardar la porción de la imagen seleccionada
# 'r' restaurar la imagen original 
# 'q' finaliza el script
# 'e' Aplica T. Euclideana a la seleccion realiza
# 's' Aplica T. de Similaridad a la seleccion
#**************************************************
# 'a' Aplica T. Affine a 3 puntos seleccionados
# Esta transformacion se guarda solo al pulsar 'g'
#**************************************************
# 'h' T. Homografia a 4 puntos seleccionados
# Esta transformacion se guarda solo al pulsar 'g'
#**************************************************
#
# El script lee la imagen 'rpi.jpg' y 'ne555.jpg'
# y guarda las modificaciones como 'tmp/{:04}.png'
# Los parametros de Transformacion son constantes
#**************************************************
import os
import shutil
import cv2
import numpy as np
import transform

dir = 'tmp'
if(os.path.exists(dir)):
    shutil.rmtree(dir)
if(not os.path.exists(dir)):
    os.mkdir(dir)
output_file = '{}/{:04}.png'
cont = 0
#----------------------------------------------------
angulo = 45	    # parametros de la Transformacion
tx = 15
ty = 70
escala = 2.5
#----------------------------------------------------
blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False         # True si mouse el mouse es presionado
sel_puntos = False      # para la seleccion de puntos en transformaciones
t_a = False             # True: realizando una Affine
t_h = False             # True: realizando una Homografia
xybutton_down = -1, -1  # coordenadas al hacer click izq.
xybutton_up = -1, -1    # coordenadas al soltar 
puntos = []             # lista de puntos seleccionados
img_in = 'rpi.jpg'
chip = 'ne555.jpg'
title_img = 'Imagen a procesar'

img = cv2.imread(img_in,1)
alto,ancho = img.shape[:2]
print('Imagen -> H: {0}, W: {1}'.format(alto,ancho))
img_chip = cv2.imread(chip,1)
alto2,ancho2 = img_chip.shape[:2]
print('Img_chip -> H: {0}, W: {1}'.format(alto2,ancho2))

img2 = np.zeros((alto, ancho, 3), np.uint8)
# hago una copia de la original para restaurar 
img2[:] = img[:]                            
    
#**************************************************
# Funcion para guardar el recorte de la img.
#**************************************************
def guardar(imagen):
    global cont
    cv2.imwrite(output_file.format(dir,cont),imagen)
    cont+=1
    
#***************************************************
# Calculo el tamaño de la nueva imagen seleccionada
#
# Return: la porcion de la imagen seleccionada
#***************************************************
def seleccion():
    # Evito valores negativos al hacer al soltar el click
    # fuera de la ventana
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
    img_sel = np.zeros((y, x, 3), np.uint8)
    print('tamaño seleccion -> W: {0}, H: {1}'.format(x, y))
    img_sel = img2[altoi:altof, anchoi:anchof]
    return img_sel
    
#***************************************************
# Funcion de callback para eventos del mouse
#***************************************************
def draw_cut(event, x, y, flags, param):
    global xybutton_down, xybutton_up, drawing, sel_puntos, puntos
    if event == cv2.EVENT_LBUTTONDOWN:
        if(sel_puntos):
            cv2.circle(img,(x,y),2,green,1)
            puntos.append([x,y])
        else:
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

#**************************************************
# Funcion T. Affine al recorte de la img.
#**************************************************
def affine(puntos):
    cv2.line(img,tuple(puntos[0]),tuple(puntos[1]),blue,1)  # marco la seleccion
    cv2.line(img,tuple(puntos[1]),tuple(puntos[2]),blue,1)
    pts1 = np.float32([puntos])
    print('Param. de T. Affine -> p1: {0}, p2: {1}, p3: {2}'
              .format(puntos[0], puntos[1], puntos[2]))
    
    p_chip = np.float32([[158,0],[0,0],[0,154]])
    mask = np.ones((alto2, ancho2, 3), np.float32) * 255
            
    A = cv2.getAffineTransform(p_chip, pts1)
    ta = cv2.warpAffine(img_chip, A, (ancho, alto))
    tmask = cv2.warpAffine(mask, A, (ancho, alto))
    
    resta = cv2.subtract(img2, np.uint8(tmask))
    afin = cv2.add(resta, np.uint8(ta))
    cv2.imshow('Transformada Affine',afin)
    
    return afin
    
#**************************************************
# Funcion T. Homografia al recorte de la img.
#**************************************************
def homografia(puntos):
    cv2.line(img,tuple(puntos[0]),tuple(puntos[1]),blue,1)  # enmarco la seleccion
    cv2.line(img,tuple(puntos[1]),tuple(puntos[3]),blue,1)
    cv2.line(img,tuple(puntos[2]),tuple(puntos[3]),blue,1)
    cv2.line(img,tuple(puntos[0]),tuple(puntos[2]),blue,1)
    pts1 = np.float32([puntos])
    print('Homografia -> p1: {0}, p2: {1}, p3: {2}, p4: {3}'
                  .format(puntos[0], puntos[1], puntos[2], puntos[3]))
          
    p_out = np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
                
    H = cv2.getPerspectiveTransform(pts1, p_out)
    th = cv2.warpPerspective(img2, H, (ancho, alto))
        
    cv2.imshow('Homografia',th)
    
    return th
    
#**************************************************
cv2.imshow(title_img,img)
cv2.setMouseCallback(title_img, draw_cut)

while(1):
    cv2.imshow(title_img, img)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('g'):      # guardar la porción de la imagen seleccionada
        if(sel_puntos and t_a):
            guardar(afin)
        elif(sel_puntos and t_h):
            guardar(homog)            
        else:
            guardar(seleccion())        

    if k == ord('e'):      # T. Euclidiana la porción de la imagen seleccionada        
        print('Param. de T. Euclidiana -> tx: {0}, ty: {1}, angulo: {2}º'
              .format(tx, ty, angulo))
        te = transform.euclidea(seleccion(), angulo, tx, ty)
        guardar(te)        
    
    if k == ord('s'):      # T. de similaridad la porción de la imagen seleccionada        
        print('Param. de T. Similaridad -> tx: {0}, ty: {1}, angulo: {2}º, escala: {3}'
              .format(tx, ty, angulo, escala))
        ts = transform.similarity(seleccion(), angulo, tx, ty, escala)
        guardar(ts)        
 
    if k == ord('a'):      # T. Affine la porción de la imagen seleccionada        
        img[:] = img2[:]
        sel_puntos = True  
        t_a = True

    if k == ord('h'):      # T. Homografia la porción de la imagen seleccionada        
        img[:] = img2[:]
        sel_puntos = True
        t_h = True
                
    if k == ord('r'):      # restaurar la imagen original        
        img[:] = img2[:] 
        cv2.imshow(title_img,img)
        if(sel_puntos and t_a):
            cv2.destroyWindow('Transformada Affine')
            puntos=[]
            sel_puntos = False
            t_a = False
        if(sel_puntos and t_h):
            cv2.destroyWindow('Homografia')
            puntos=[]
            sel_puntos = False
            t_h = False
        print('Imagen restaurada')
        
    if k == ord('q'):      # finalizar el script
        print('Script finalizado correctamente')
        break
    
    if (sel_puntos):
        if (t_a and len(puntos)==3):
            afin = affine(puntos)
            puntos = []            
        if (t_h and len(puntos)==4):
            homog = homografia(puntos)
            puntos = []
#**************************************************
cv2.destroyAllWindows()
