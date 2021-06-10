#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

__version__ = '0.1'

#*************************************************
#Funcion:  Transformacion de Rotacion
#Param:    image:  es la fuente a la que se aplica
#                  la transformacion
#          angle:  angulo de rotacion
#          center: centro de rotacion
#          scale:  (por defecto mantiene la escala)
#*************************************************
def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated
#*************************************************
