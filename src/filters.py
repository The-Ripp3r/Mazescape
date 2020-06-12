import numpy as np
import cv2
import pygame as pg

def make_blurry(image):
        return pg.surfarray.make_surface(cv2.GaussianBlur(image,(9,9),0))

def make_noisy(image):
        img_cpy = image.copy()
        try:
            m = tuple(image.shape[2] * [0])
            s = tuple(image.shape[2] * [80])
        except IndexError:
            m = 0
            s = 30

        cv2.randn(img_cpy, m, s)

        return pg.surfarray.make_surface(cv2.add(img_cpy, image))