#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Kelsonz Fu'

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import pi as pi
from math import acos
from math import sqrt
from math import cos


class color:
    def __init__(self, filename):
        # 打开文件
        self.filename = filename
        self.im = Image.open(self.filename)
        # 获得图片属性
        self.xsize, self.ysize = self.im.size
        self.format = self.im.format
        self.mode = self.im.mode
        # 获得rgb通道
        temp = self.im.load()
        self.rgb = list()
        for j in range(self.ysize):
            for i in range(self.xsize):
                self.rgb.append((temp[i, j][0], temp[i, j][1], temp[i, j][2]))

    # 从图像中获得RGB通道值
    def get_rgb(self):
        return self.rgb

    def get_filename(self):
        return self.filename.split('.')[0]

    def handle(self):
        # 对I通道进行处理
        hsi = self.rgb2hsi()
        new_hsi = self.handle_i(hsi)
        self.new_rgb = self.hsi2rgb(new_hsi)
        return self.new_rgb

    # 保存
    def print_change(self):
        self.im.putdata(self.new_rgb)
        fname = 'aim.%s' % self.format
        self.im.save(fname)
        return fname

    # RGB转HSI
    def rgb2hsi(self):
        hsi = list()
        length = len(self.rgb)
        for i in range(length):
            r = self.rgb[i][0]
            g = self.rgb[i][1]
            b = self.rgb[i][2]
            if r == g and g == b:
                theta = pi / 2
                s = 0
            else:
                theta = acos(((r - g) + (r - b)) / (2 * sqrt((r - g) * (r - g) + (r - b) * (g - b))))
                s = 1 - (3 * min(r, g, b)) / (r + g + b)
            if b > g:
                h = 2 * pi - theta
            else:
                h = theta
            i = (r + g + b) / 3
            hsi.append([h, s, i])

        return hsi

    # 计算累计频率
    def sum_p(self, x, index):
        sum = 0
        for i in range(index + 1):
            sum += x[i]
        return sum

    # 处理I通道
    # 返回I通道均衡化后的hsi
    def handle_i(self, hsi):
        length = len(hsi)
        # 频数统计
        self.n = [0] * 256
        for i in range(length):
            self.n[round(hsi[i][2])] += 1
        # 频率计算
        p = [0] * 256
        for i in range(256):
            p[i] = self.n[i] / length
        # 累计频率计算
        cp = [0] * 256
        for i in range(256):
            cp[i] = self.sum_p(p, i)
        # 计算映射后的灰度值
        # new数组，索引与值分别代表映射前后的灰度值
        self.new = [0] * 256
        for i in range(256):
            self.new[i] = round(255 * cp[i])
        # 将映射后的频数对应起来，获得均衡化后的频数
        # yy数组，索引与值分别代表映射后的灰度值和频数
        self.yy = [0] * 256
        flag = self.new[0]
        for i in range(256):
            if flag != self.new[i]:
                self.yy[self.new[i]] = self.n[i]
                flag = self.new[i]
            else:
                self.yy[flag] += self.n[i]

        # 修改映射后的I值
        for i in range(length):
            hsi[i][2] = self.new[round(hsi[i][2])]
        return hsi

    # 绘直方图
    def print_Histogram(self):
        # x: 原灰度值
        x = np.arange(0, 256)
        # y: 原频数
        # yy: 映射后频数
        y = np.asarray(self.n)
        yy = np.asarray(self.yy)

        # 直方图
        plt.xlabel("r")
        plt.ylabel("s")
        plt.bar(x, y, label='old')
        plt.bar(x, yy, label='new')
        plt.legend()

        # 保存图像
        plt.savefig(self.get_filename() + '_Histogram')
        plt.show()

    # 绘灰度变换曲线
    def print_curve(self):
        # x: 原灰度值
        # new: 映射后灰度值
        x = np.arange(0, 256)
        new = np.asarray(self.new)
        # 灰度值变换曲线
        plt.xlabel('old')
        plt.ylabel('new')
        plt.plot(x, new)

        # 保存图像
        plt.savefig(self.get_filename() + '_curve')
        plt.show()

    def print_whole(self):
        # x: 原灰度值
        # new: 映射后灰度值
        x = np.arange(0, 256)
        new = np.asarray(self.new)
        # y: 原频数
        # yy: 映射后频数
        y = np.asarray(self.n)
        yy = np.asarray(self.yy)

        # 灰度值变换曲线
        plt.subplot(2, 1, 2)
        plt.xlabel('old')
        plt.ylabel('new')
        plt.plot(x, new)

        # 直方图
        plt.subplot(2, 1, 1)
        plt.xlabel("r")
        plt.ylabel("s")
        plt.bar(x, y, label='old')
        plt.bar(x, yy, label='new')
        plt.legend()

        # 保存图像
        plt.savefig(self.get_filename() + '_both')
        plt.show()

    # HSI转RGB
    def hsi2rgb(self, hsi):
        new_rgb = list()
        length = len(hsi)
        for j in range(length):
            h = hsi[j][0]
            s = hsi[j][1]
            i = hsi[j][2]
            if 0 <= h < 2 * pi / 3:
                b = i * (1 - s)
                r = i * (1 + (s * cos(h)) / (cos(pi / 3 - h)))
                g = 3 * i - (r + b)
            elif 2 * pi / 3 <= h < 4 * pi / 3:
                h = h - 2 * pi / 3
                r = i * (1 - s)
                g = i * (1 + (s * cos(h)) / (cos(pi / 3 - h)))
                b = 3 * i - (r + g)
            elif 4 * pi / 3 <= h < 2 * pi:
                h = h - 4 * pi / 3
                g = i * (1 - s)
                b = i * (1 + (s * cos(h)) / (cos(pi / 3 - h)))
                r = 3 * i - (b + g)
            r = int(round(r))
            g = int(round(g))
            b = int(round(b))
            new_rgb.append((r, g, b))
        return new_rgb


if __name__ == "__main__":
    x = color('color.jpg')
    # 进行处理
    x.handle()
    # 打印变换后图像
    x.print_change()
    # 打印灰度变换曲线和直方图
    # x.print_curve()
    # x.print_Histogram()
    x.print_whole()
