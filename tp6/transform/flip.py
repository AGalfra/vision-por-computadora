#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

__version__ = '0.1'

# modes selecciona el eje de espejado en el metodo .flip
modes = {'x': 0, 'y': 1, 'b': -1}
#*************************************************
# Funcion: Transformacion de Espejado
# Param: img: es la fuente a la que se aplica
#                la transformacion
#        mode: es el eje de espejado
#*************************************************
def flip(img, mode):
    if(mode not in modes.keys()):
        return img

    flipped = cv2.flip(img, modes[mode])
    return flipped
#*************************************************
