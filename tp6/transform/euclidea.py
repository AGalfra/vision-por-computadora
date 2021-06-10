#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

__version__ = '0.1'
#*************************************************
#Funcion:  Transformacion Euclidaina
#Param:    image:  es la fuente a la que se aplica
#                  la transformacion
#          angle:  angulo de rotacion
#          tx, ty: las corrdenadas de destino 
#*************************************************
def euclidea(image, angle, tx, ty):
    
    R = cv2.getRotationMatrix2D((0,0), angle, scale=1.0)
    
    M = np.float32([[R[0,0], R[0,1], tx],
                    [R[1,0], R[1,1], ty]])
                    
    (h , w) = image.shape[:2]
    euclidean = cv2.warpAffine(image, M, (w, h))
           
    return euclidean
#*************************************************
