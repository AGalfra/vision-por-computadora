#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2

__version__ = '0.1'

#*************************************************
# Funcion: Transformacion de translacion
# Param: image: es la fuente a la que se aplica
#                la transformacion
#         x, y: las corrdenadas de destino 
#*************************************************
def translate(image, x, y):
    (h , w) = image.shape[:2]
    M = np.float32([[1, 0, x],
                    [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (w, h))
    return shifted
#*************************************************
