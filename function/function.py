# encoding: utf8

import os

from PIL import Image
# imports
from PyQt5.QtGui import QPixmap

from function.basic import exp
from function.color import color
from function.grey import grey
from function.hence import ImageFilter


class function:
    def __init__(self):
        pass

    @staticmethod
    def rotate(filename: str, degree: float):
        img = exp(filename)
        img.rotate(degree)
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def move(filename: str, X, Y):
        img = exp(filename)
        img.move(X, Y)
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def flip(filename: str, axis: str):
        img = exp(filename)
        img.flip(axis)
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def zoom(*args):
        img = exp(args[0])
        if len(args) == 3:
            img.resize((args[1], args[2]))
        elif len(args) == 2:
            img.resize(args[1])
        fname = img.save()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def medial_filter(filename: str, size: int):
        img = ImageFilter(filename)
        fname = img.medial_filter(size=size)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def avg_filter(filename: str, size: int):
        img = ImageFilter(filename)
        fname = img.avg_filter(size=size)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
        pass

    @staticmethod
    def robert(filename: str, hence: bool):
        img = ImageFilter(filename)
        fname = img.robert(hence)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def prewitt(filename: str, hence: bool):
        img = ImageFilter(filename)
        fname = img.prewitt(hence)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def sobel(filename: str, hence: bool):
        img = ImageFilter(filename)
        fname = img.sobel(hence)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def laplace(filename: str, area: int, hence: bool):
        img = ImageFilter(filename)
        fname = img.laplacian(area, hence)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def gauss(filename: str, sigma: float, size: int):
        img = ImageFilter(filename)
        _, fname = img.gauss(sigma, size)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def canny(filename: str, low: int, high: int):
        img = ImageFilter(filename)
        fname = img.canny(low=low, high=high)
        pix = QPixmap(fname)
        os.remove(fname)
        return pix

    @staticmethod
    def his(filename: str):
        im = Image.open(filename)
        if im.mode == 'L':
            im = grey(filename)

        else:
            im = color(filename)
        im.handle()
        fname = im.print_change()
        pix = QPixmap(fname)
        os.remove(fname)
        return pix
